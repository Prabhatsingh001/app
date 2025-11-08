# StudyBuddy — API-driven Django project

This repository is a Django project that provides features for student workflows: account management, profile/dashboard, uploading and viewing notes/question papers, a CGPA calculator, summaries, and feedback APIs. It uses Django REST Framework with JWT authentication.

## Key components

- Django project module: `app`
- Apps included:
	- `studybudy` — custom user model and auth/profile views
	- `UploadNotesOrQuestionPaper` — upload & view notes and question papers
	- `CgCalculator` — CGPA calculation endpoint
	- `feedback` — feedback API
	- `summarize` — (text summarization views)
- API routing: `api/urls.py` exposes auth, profile, notes, feedback and utility endpoints
- Database: SQLite (default `db.sqlite3`)
- Auth: JWT (djangorestframework-simplejwt)

## Prerequisites

- Python 3.10+ (project uses Django 5.x; ensure a compatible Python version)
- Windows PowerShell (commands below are PowerShell-friendly)
- Recommended: create and use a virtual environment

## Installation (Windows PowerShell)

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3. Create a `.env` file at the project root or set environment variables. The project uses python-decouple.

Example `.env`:

```
SECRET_KEY=your-secret-key
DEBUG=True
```

4. (Optional) If running in production, set `DEBUG=False` and configure `ALLOWED_HOSTS` in `app/settings.py` or via environment variables.

## Database & media

- Default DB: `db.sqlite3` in the project root. No DB credentials are required for local development.
- Uploaded files are stored in the `media/` directory (check `MEDIA_ROOT` in `app/settings.py`).

## Run migrations and start server

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Server will be available at http://127.0.0.1:8000/ by default.

## Authentication and API

This project uses JWT authentication through `rest_framework_simplejwt`. Default REST permission requires authentication.

Important endpoints (from `api/urls.py`):

- Auth:
	- `api/signup/` — user signup
	- `api/login/` — login
	- `api/logout/` — logout
	- `api/change_password/` — change password
- Profile:
	- `api/dashboard/` — user dashboard
	- `api/update_profile/` — update profile
	- `api/delete_profile/` — delete profile
	- `api/delete_profile_picture/` — delete profile picture
- Notes & Question Papers:
	- `api/upload_notes/` — upload notes
	- `api/upload_question_paper/` — upload question paper
	- `api/view_notes/` — view notes
	- `api/get_question_paper/` — list/get question papers
- Feedback:
	- `api/feedback/` — feedback submission (class-based API view)
- Utilities:
	- `api/token/refresh/` — refresh JWT token
	- `api/calculate-cgpa/` — CGPA calculation (class-based API view)

Note: these paths are relative to where `api` is included in your root `app/urls.py`. If `api/` path is prefixed, the actual URLs will reflect that prefix (e.g., `/api/signup/`).

## Tests

Run the test suite with:

```powershell
python manage.py test
```

## Environment & settings notes

- Settings are in `app/settings.py`. The project expects a `SECRET_KEY` provided via `python-decouple` (`.env`) or environment variables.
- `AUTH_USER_MODEL` is set to `studybudy.CustomUser`.
- REST framework global settings require authentication by default. Adjust `REST_FRAMEWORK` in settings if you want some endpoints publicly accessible.

## Troubleshooting

- If you see import errors, ensure the virtual environment is activated and `pip install -r requirements.txt` completed successfully.
- For missing SECRET_KEY errors, create a `.env` with SECRET_KEY or set the environment variable in PowerShell:

```powershell
$env:SECRET_KEY = 'some-secret-key'
$env:DEBUG = 'True'
```

