from fastapi import FastAPI, Request
from dictionary_api import word_info
from word_day_api import word_of_the_day
from trending_api import trending_words
from ip_history_api import get_ip, export_history, add_word_to_history, history_page

app = FastAPI()

@app.get("/app/healthy")
def health():
    return {"system": "success"}

@app.get("/app/words/{word}")
def word_end(word: str, request: Request):
    ip = get_ip(request)
    add_word_to_history(ip, word)
    return word_info(word)
    

@app.get("/app/trending/{word}")
def trending_end(word: str):
    return trending_words(word)

@app.get("/app/word_of_the_day")
def daily_word_end():
    return word_of_the_day()

@app.get("/history")
def history_list(req: Request, limit: int = 10, page: int = 1):
    ip = get_ip(req)
    if not ip:
        return {"error": "IP Not Found. Please check your request."}
    return history_page(ip, limit, page)

@app.get("/history/export")
def export_end(req: Request, format: str = "json"):
    ip = get_ip(req)
    if not ip:
        return {"error": "IP Not Found. Please check your request."}

    return export_history(ip, format.lower())
