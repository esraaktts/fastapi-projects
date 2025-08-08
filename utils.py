from datetime import datetime, timezone
from fastapi import Request

def get_ip(reqst: Request):
    if reqst.client:
        return reqst.client.host
    return None

def get_timestamp():
    return datetime.now(timezone.utc).isoformat()
