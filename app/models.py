from pydantic import BaseModel, EmailStr, AnyUrl, constr
from typing import Annotated
from typing import Optional

class MailRequest(BaseModel):
    # User's name: required, 5–100 chars, strips whitespace
    name: Annotated[str, constr(strip_whitespace=True, min_length=5, max_length=100)]
    
    # Email: required, validated as proper email
    email: EmailStr
    
    # Message: required, 10–1000 chars, strips whitespace
    message: Annotated[str, constr(strip_whitespace=True, min_length=10, max_length=1000)]
    
    # Site: optional, 20–100 chars
    site: AnyUrl
    
    # Service: optional, 1–100 chars if provided
    service: Annotated[str | None, constr(strip_whitespace=True, min_length=10, max_length=100)] = None
    
    # Honeypot: optional, must be empty (spam detection)
    monkeybusiness: Annotated[str, constr(strip_whitespace=True, max_length=100)] = ""

    # reCAPTCHA token: required, non-empty string (if used)
    recaptcha_token: str