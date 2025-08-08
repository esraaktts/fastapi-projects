from redis import Redis
import json
from datetime import datetime, timezone
from fastapi import HTTPException, Request

def get_ip(reqst: Request):
    if reqst.client:
        return reqst.client.host
    else:
        return None

def get_timestamp():
    return datetime.now(timezone.utc).isoformat()

def get_history(ip: str, r: Redis):
    history = r.hget("history", ip)
    if history:
        return json.loads(history)
    else:
        return []

def add_word_to_history(ip: str, word: str, r: Redis):
    history = get_history(ip,r)
    history.append({
        "word": word,
        "timestamp": get_timestamp()
    })
    r.hset("history", ip, json.dumps(history))

def history_page(ip: str, r: Redis, limit=10, page=1):
    all_data = get_history(ip, r)
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

def export_history(ip: str,r: Redis, format: str = "json"):
    data = get_history(ip,r) or []

    if format == "json":
        return data

    elif format == "csv":
        lines = ["time,word"] + [f'{d["timestamp"]},{d["word"]}' for d in data]
        return "\n".join(lines)

    elif format == "txt":
        lines = [f'{d["timestamp"].replace("T", " ").split(".")[0]} - {d["word"]}' for d in data]
        return "\n".join(lines)

    else:
        raise HTTPException(status_code=400, detail="Unsupported export format. Please use json, csv, or txt.")
