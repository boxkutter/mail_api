# Mail API

A FastAPI-based mail API service that enables websites to send contact us emails using an SMTP server. This service provides a secure, rate-limited endpoint with built-in spam protection through reCAPTCHA verification and honeypot fields.

## Features

- **SMTP Integration**: Sends emails via configurable SMTP server
- **Rate Limiting**: Prevents abuse with configurable rate limits (default: 5 requests per minute)
- **Spam Protection**: Includes reCAPTCHA verification and honeypot fields
- **API Key Authentication**: Secures access with API keys per site
- **CORS Support**: Configurable allowed origins for web integration
- **Logging**: Comprehensive logging for monitoring and debugging
- **Docker Ready**: Easy deployment with Docker Compose

## Prerequisites

- Docker and Docker Compose
- SMTP server credentials
- Google reCAPTCHA v2 secret key
- API keys for client websites

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mail_api
   ```

2. Copy the environment file and configure it:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` with your configuration:
   ```env
   # SMTP Configuration
   SMTP_HOST=your-smtp-host.com
   SMTP_PORT=587
   SMTP_TLS=true
   SMTP_USER=your-smtp-username
   SMTP_PASS=your-smtp-password

   # Mail Routing
   MAIL_FROM=noreply@yourdomain.com
   MAIL_TO=contact@yourdomain.com

   # Security
   MAIL_API_KEY=your-api-key-here

   # CORS
   ALLOWED_ORIGINS=http://localhost:3000,https://yourwebsite.com

   # reCAPTCHA
   RECAPTCHA_SECRET=your-recaptcha-secret-key
   ```

## Running the Application

### Development
```bash
docker compose up --build
```

### Production
```bash
docker compose up -d --build
```

### Updating
```bash
git pull
docker compose up -d --build
```

## API Usage

### Endpoint

**POST /send**

Sends a contact email using the configured SMTP server.

#### Headers
- `x-api-key`: Your API key (required)
- `Content-Type`: application/json

#### Request Body
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Hello, I have a question about your service.",
  "site": "https://example.com",
  "service": "General Inquiry",
  "recaptcha_token": "recaptcha-response-token",
  "monkeybusiness": ""
}
```

#### Field Descriptions
- `name` (string, required): Sender's name (5-100 characters)
- `email` (string, required): Sender's email address (must be valid email)
- `message` (string, required): Message content (10-1000 characters)
- `site` (string, required): Website URL where the form was submitted
- `service` (string, optional): Service or department (10-100 characters if provided)
- `recaptcha_token` (string, required): reCAPTCHA v2 response token
- `monkeybusiness` (string, optional): Honeypot field - leave empty

#### Response
**Success (200):**
```json
{
  "success": true,
  "version": "1.0.2"
}
```

**Error Responses:**
- `400`: Bad Request (invalid data, reCAPTCHA failed, bot detected)
- `401`: Unauthorized (invalid API key)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error

#### Example Usage (JavaScript)
```javascript
const response = await fetch('https://your-mail-api.com/send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': 'your-api-key'
  },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    message: 'Hello!',
    site: 'https://example.com',
    recaptcha_token: 'recaptcha-token-here',
    monkeybusiness: ''
  })
});

const result = await response.json();
```

## Configuration

All configuration is done via environment variables in the `.env` file:

- **SMTP_HOST**: SMTP server hostname
- **SMTP_PORT**: SMTP server port (usually 587 for TLS)
- **SMTP_TLS**: Enable TLS encryption (true/false)
- **SMTP_USER**: SMTP username
- **SMTP_PASS**: SMTP password
- **MAIL_FROM**: From email address for sent emails
- **MAIL_TO**: Destination email address for contact forms
- **MAIL_API_KEY**: API key for authentication
- **ALLOWED_ORIGINS**: Comma-separated list of allowed CORS origins
- **RECAPTCHA_SECRET**: Google reCAPTCHA v2 secret key

## Security

- API key authentication required for all requests
- Rate limiting to prevent abuse
- reCAPTCHA verification to block bots
- Honeypot field for additional spam detection
- CORS restrictions to allowed origins only

## Logging

The application logs all requests and errors. Logs include:
- Request timestamps and client IPs
- Email sending attempts
- Rate limit violations
- reCAPTCHA failures
- Bot detection events

## Development

For local development:
1. Set up your `.env` file
2. Run `docker compose up --build`
3. The API will be available at `http://localhost:8000`
4. API documentation at `http://localhost:8000/docs`
