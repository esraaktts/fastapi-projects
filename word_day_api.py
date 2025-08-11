import json
from app.models.models import DailyResponse
from redis import Redis, exceptions
from fastapi import HTTPException

def word_of_the_day(r: Redis):
    try:
        daily_word = r.get("word_of_the_day")
        if daily_word and isinstance(daily_word, bytes):
            daily_word = daily_word.decode()

        if daily_word:
            word_redis = r.get(f"random_word:{daily_word}")
            if word_redis:
                word_data = json.loads(word_redis)
                return DailyResponse(
                    word=daily_word,
                    definition=word_data.get("meaning"),
                    tags=word_data.get("tags", [])
                )
            else:
                return DailyResponse(
                    word=daily_word,
                    definition=None,
                    tags=None,
                    title="Incomplete Data",
                    message=f"Details for '{daily_word}' not found in Redis.",
                    resolution="Please try again later."
                )
        else:
            word_json = r.srandmember("words_unused")
            if not word_json:
                return DailyResponse(
                    word=None,
                    definition=None,
                    tags=None,
                    title="No Words Available",
                    message="No unused words left in Redis.",
                    resolution="Please add more words or reset used words."
                )
            word_data = json.loads(word_json)
            selected_word = word_data["word"]

            r.srem("words_unused", word_json)
            r.sadd("words_used", word_json)

            r.set("word_of_the_day", selected_word, ex=86400)
            r.set(f"random_word:{selected_word}", word_json, ex=86400)

            return DailyResponse(
                word=selected_word,
                definition=word_data.get("meaning"),
                tags=word_data.get("tags", [])
            )

    except Exception:
        raise HTTPException(status_code=503, detail="Redis connection failed.")

