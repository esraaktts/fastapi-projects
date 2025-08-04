import redis
import json
import random
from models import DailyResponse

def word_of_the_day():
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)

        selected_word = r.get("daily_word")

        if selected_word:
            word_redis = json.loads(selected_word)
            return word_redis

        else:
            print("No word of the day found in Redis, generating a new one.")
            
            with open('saved_words.json', 'r') as file:
                word_list = json.load(file)
                
            random_word = random.choice(word_list)
            new_word = {
                "word": random_word["word"],
                "definition": random_word["meaning"],
                "tags": random_word["tags"]
            }

            r.set("daily_word", json.dumps(new_word),ex=86400)
            print("New word of the day set in Redis.")               
            return new_word

    except Exception:
        return DailyResponse(
            word = None,
            definition = None,
            tags=None,
            title = "Service Unavailable",
            message = "we couldn't locate a definition for the word you entered.",
            resolution = "Please try again later."
        )
