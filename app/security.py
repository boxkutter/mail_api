from fastapi import Request, HTTPException
from app.config import settings

def verify_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if not key or key not in settings.api_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")
