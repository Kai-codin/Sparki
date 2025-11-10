# Sparki
Sparki - Minimal Flask app

This repository contains a tiny Flask app used as a starting point.

Files added:
- `app.py` - the Flask application.
- `requirements.txt` - Python dependencies (Flask, pytest).
- `tests/test_app.py` - small pytest suite for basic endpoints.

Quick start (zsh):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Run tests
pytest -q
# Run the app
python app.py
```

Endpoints:
- `GET /` -> JSON welcome message
- `GET /health` -> health check
- `POST /echo` -> echoes JSON payload back

Next steps:
- Add more routes and documentation
- Add CI to run tests automatically
