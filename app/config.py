from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # SMTP
    smtp_host: str
    smtp_port: int
    smtp_tls: bool = True
    smtp_user: str
    smtp_pass: str

    # Mail routing
    mail_from: str
    mail_to: str

    # Security
    mail_api_key: str

    # CORS
    allowed_origins: List[str]

    # App
    version: str = "1.0.0"

    # reCAPTCHA
    recaptcha_secret: str

    class Config:
        env_file = ".env"
        extra = "forbid"


settings = Settings()
