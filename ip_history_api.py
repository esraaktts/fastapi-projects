import redis
import json
from datetime import datetime, timezone
from fastapi import Request

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_ip(reqst: Request):
    if reqst.client:
        return reqst.client.host
    else:
        return None

def get_timestamp():
    return datetime.now(timezone.utc).isoformat()

def get_history(ip: str):
    history = r.hget("history", ip)
    if history:
        return json.loads(history)
    else:
        return []

def add_word_to_history(ip: str, word: str):
    history = get_history(ip)
    history.append({
        "word": word,
        "timestamp": get_timestamp()
    })
    r.hset("history", ip, json.dumps(history))

def get_full(ip: str):
    return get_history(ip)

def export_history(ip, format="json"):
    data = get_history(ip)
    if not data:
        data = []

    if format == "json":
        return data

    elif format == "csv":
        csv_lines = []
        for i in range(len(data)):
            time_stamp = data[i]["timestamp"]
            word = data[i]["word"]
            csv_lines.append(time_stamp + "," + word)
        csv_text = "time,word\n" + "\n".join(csv_lines)

        return {"export": csv_text.strip()}

    elif format == "txt":
        text = []
        for i in range(len(data)):
            time_stamp = data[i]["timestamp"]
            word = data[i]["word"]
            time_str = time_stamp.replace("T", " ").split(".")[0]
            text.append(f"{time_str} - {word}")
            
        return {"export": "\n".join(text)}

    else:
        return {"Error": "Wrong format. Please use json, csv or txt."}

def history_page(ip, limit=10, page=1):
    all_data = get_history(ip)
    if not all_data:
        all_data = []

    start = (page - 1) * limit
    end = start + limit

    part = all_data[start:end]

    return {
        "page": page,
        "limit": limit,
        "total": len(all_data),
        "data": part
    }
