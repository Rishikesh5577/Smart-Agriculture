# Smart Agriculture (Django)

Smart Agriculture is an IoT + Machine Learning web app for crop prediction and fertilizer recommendation. It uses real-time or user-provided inputs, ML models, and a simple chatbot to assist farmers and agronomists.

## Features
- **User auth**: Register, login, dashboard.
- **Crop prediction**: Predict optimal crop from soil and weather parameters.
- **Fertilizer recommendation**: Recommend fertilizer based on inputs.
- **Reports**: View latest predictions and details.
- **Chatbot**: Optional Gemini-powered Q&A (requires Google API key).

## Tech Stack
- **Backend**: Django 4.1.x, Python 3.11+ (tested with 3.13)
- **Database**: SQLite (dev)
- **ML**: Pre-trained `.pkl` models (Naive Bayes)
- **Frontend**: Django templates + static assets (Bootstrap, jQuery)

## Project Structure
```
Smart-Agriculture/
├─ app/                     # Django app (views, models, urls)
├─ crop_prediction/         # Project settings and urls
├─ dataset/                 # ML model files (*.pkl)
├─ static/                  # CSS/JS/images
├─ templates/               # HTML templates
├─ manage.py
└─ requirements.txt
```

## Prerequisites
- Python 3.11+ (Python 3.13 supported)
- Pip
- (Optional) Virtual environment tool like `venv` or `conda`

## Setup (Windows / PowerShell)
1) Clone and enter the project folder.
2) Create and activate a virtual environment (recommended):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
3) Install dependencies:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4) Apply database migrations:
```powershell
python manage.py migrate
```
5) (Optional) Create admin user:
```powershell
python manage.py createsuperuser
```
6) Run the development server:
```powershell
python manage.py runserver
```
Then open http://127.0.0.1:8000/

## Environment Configuration
For development, the project defaults to Django’s console email backend (emails are printed to terminal). To use real email (Gmail SMTP), configure environment variables and enable SMTP in `crop_prediction/settings.py`.

Example PowerShell environment setup for this session:
```powershell
# Django
$env:DEBUG = "True"

# Gmail (Production-like usage)
$env:EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
$env:EMAIL_HOST = "smtp.gmail.com"
$env:EMAIL_PORT = "465"    # SSL
$env:EMAIL_USE_SSL = "True"
$env:EMAIL_HOST_USER = "<your_gmail_address>"
$env:EMAIL_HOST_PASSWORD = "<your_app_password>"  # Use an App Password

# Chatbot (Gemini) – optional
$env:GOOGLE_API_KEY = "<your_google_api_key>"
```

Note: For Gmail, use an App Password, not your regular password.

## Chatbot (Gemini) Setup
The chatbot endpoint relies on Google’s Generative AI SDK.
- Dependency: `google-generativeai` (already listed in `requirements.txt`). If missing, install:
```powershell
pip install google-generativeai
```
- Set `GOOGLE_API_KEY` in your environment before starting the server.
- The function `app/modify.py:modify_msg()` lazily initializes the Gemini client and will return a helpful message if the key or package is missing.

## Static Files (Development)
- Static files are served from `static/` during development.
- Paths are referenced via the Django `{% static %}` tag in templates (see `templates/base.html`).
- If you still see 404s for optional plugins, CDN fallbacks are included.

## Troubleshooting
- **Duplicate username on registration**: You’ll see a friendly message if the email/username already exists.
- **Email errors on Python 3.13**: Django’s SMTP backend may hit TLS/SSL incompatibilities. The project defaults to the console email backend for development. Switch to Gmail SMTP with SSL on port 465 in production.
- **Chatbot not responding**: Ensure `google-generativeai` is installed and `GOOGLE_API_KEY` is set. Check server console for messages from `modify_msg()`.
- **Static 404s**: Hard refresh (Ctrl+F5). Ensure files exist under `static/` and templates use `{% load static %}`.

## Security
- Never commit API keys, passwords, or secrets to the repo.
- Prefer environment variables or a secrets manager for production.

## License
Add your preferred license here (e.g., MIT).

## Contributing
Pull requests are welcome. For major changes, open an issue first to discuss what you’d like to change.
