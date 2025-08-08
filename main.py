from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import Response
from redis import Redis
from app.api.trending_api import trending_words, add_word_to_trending
from app.api.ip_history_api import export_history, add_word_to_history, history_page
from app.api.dictionary_api import word_info
from app.models.models import TrendingResponse, DailyResponse, HistoryPageResponse, WordResponse
from app.core.utils import get_ip
from app.core.redis_client import get_redis_client
from app.api.word_day_api import word_of_the_day

app = FastAPI()

def get_redis():
    return get_redis_client()

@app.get("/app/healthy")
def health():
    return {"system": "success"}

@app.get("/app/words/{word}", response_model=WordResponse)
def word_end(
    word: str,
    request: Request,
    r: Redis = Depends(get_redis)
):
    ip = get_ip(request)
    add_word_to_history(ip, word, r)
    add_word_to_trending(word, r)
    return word_info(word, r)
    
@app.get("/app/trending", response_model=TrendingResponse)
def trending_end(r: Redis = Depends(get_redis)):
    try:
        return trending_words(r)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trending error: {str(e)}")


@app.get("/app/word_of_the_day", response_model=DailyResponse)
def daily_word_end(r: Redis = Depends(get_redis)):
    return word_of_the_day(r)

@app.get("/app/history", response_model=HistoryPageResponse)
def history_list(
    request: Request,
    limit: int = 10,
    page: int = 1,
    r: Redis = Depends(get_redis)
):
    ip = get_ip(request)
    if not ip:
        raise HTTPException(status_code=400, detail="IP Not Found. Please check your request.")
    return history_page(ip, limit=limit, page=page, r=r)

@app.get("/app/history/export")
def export_end(
    request: Request,
    format: str = "json",
    r: Redis = Depends(get_redis)
):
    ip = get_ip(request)
    if not ip:
        raise HTTPException(status_code=400, detail="IP Not Found. Please check your request.")
    
    f = format.lower()
    supported_formats = {"json", "csv", "txt"}

    if f not in supported_formats:
        raise HTTPException(status_code=400, detail="Unsupported export format. Please use json, csv, or txt.")

    data = export_history(ip, r, f)

    if f == "json":
        return JSONResponse(content=data)
    
    file_type = "text/csv" if f == "csv" else "text/plain"
    filename = f"history_{ip}.{f}"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}

    return Response(content=data, media_type=file_type, headers=headers)
