from aiosmtplib import SMTP
from app.config import settings
from app.models import MailRequest

async def send_mail(data: MailRequest):
    smtp = SMTP(
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        start_tls=settings.smtp_tls,
    )

    await smtp.connect()
    await smtp.login(settings.smtp_user, settings.smtp_pass)

    message = f"""From: {settings.mail_from}
To: {settings.mail_to}
Reply-To: {data.email}
Subject: [{data.site}] New enquiry from {data.name}

Name: {data.name}
Email: {data.email}

{data.message}
"""

    await smtp.sendmail(
        settings.smtp_user,
        [settings.mail_to],
        message
    )

    await smtp.quit()
