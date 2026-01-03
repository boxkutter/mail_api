from fastapi import Header, HTTPException
from app.config import settings

async def require_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != settings.mail_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
