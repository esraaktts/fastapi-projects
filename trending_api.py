import redis
import json

def trending_words(word: str):
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        trending_string = r.get("trending")

        if trending_string:
            counts = json.loads(trending_string)
        else:
            counts = {}

        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

        r.set("trending", json.dumps(counts))

        trending_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
        print("Trending words (top 10):")
        for word, count in trending_words:
            print(f"{word}:{count}")

        return {"Trending Words:": dict(trending_words)} 

    except Exception:
        print("Please check the Redis server connection and ensure it is running.")