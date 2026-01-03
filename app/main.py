from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.models import MailRequest
from app.mailer import send_mail
from app.deps import require_api_key

from pydantic import BaseModel, HttpUrl, constr
import httpx
import os

# ---------------------
# Logging
# ---------------------
APP_VERSION = settings.version
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mail-api")

# ---------------------
# Lifespan handler
# ---------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 Mail API starting — version {APP_VERSION}")
    yield
    logger.info("🛑 Mail API shutting down")

# ---------------------
# App initialization
# ---------------------
app = FastAPI(title="Mail API", version=APP_VERSION, lifespan=lifespan)

# Environment variable for secret key
RECAPTCHA_SECRET = settings.recaptcha_secret
if not RECAPTCHA_SECRET:
    logger.warning("RECAPTCHA_SECRET is not set in environment variables.") 



# ---------------------
# CORS setup
# ---------------------
if isinstance(settings.allowed_origins, str):
    origins = [o.strip() for o in settings.allowed_origins.split(",")]
else:
    origins = settings.allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------
# Rate limiting
# ---------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests"},
    )

# ---------------------
# Mail endpoint
# ---------------------
@app.post("/send")
@limiter.limit("5/minute")
async def send(
    payload: MailRequest,
    request: Request,
    _: None = Depends(require_api_key)
):
    # Client IP
    client_ip = request.client.host if request.client else "unknown"

    # Honeypot check
    if getattr(payload, "monkeybusiness", None):
        logger.warning(f"Blocked bot request from {client_ip}")
        raise HTTPException(status_code=400, detail="Bot detected")

    # Verify reCAPTCHA token
    recaptcha_data = {
        "secret": RECAPTCHA_SECRET,
        "response": getattr(payload, "recaptcha_token", ""),
        "remoteip": client_ip,
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://www.google.com/recaptcha/api/siteverify", data=recaptcha_data)
            result = resp.json()
    except httpx.RequestError as e:
        logger.error(f"reCAPTCHA verification failed: {str(e)}")
        raise HTTPException(status_code=500, detail="reCAPTCHA verification error")

    if not result.get("success", False):
        logger.warning(f"reCAPTCHA failed for {client_ip}")
        raise HTTPException(status_code=400, detail="reCAPTCHA verification failed")

    # Log request info
    logger.info(f"Send request from {client_ip} — {payload.name} <{payload.email}>")

    # Send the email
    await send_mail(payload)

    return {"success": True, "version": APP_VERSION}

