from redis import Redis
import json
from fastapi import HTTPException
from app.models.models import TrendingResponse

def add_word_to_trending(word: str, r: Redis):
    try:
        trending = r.get("trending")
        if trending:
            counts = json.loads(trending)
        else:
            counts = {}

        counts[word] = counts.get(word, 0) + 1
        r.set("trending", json.dumps(counts))
    except Exception:
        raise HTTPException(status_code=500, detail="Error adding word to trending list. Please try again later.")


def trending_words(r : Redis, limit: int = 10):
    trending = r.get("trending")
    if trending:
        counts = json.loads(trending)
    else:
        counts = {}
    top = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    return TrendingResponse(trending={word: count for word, count in top})
