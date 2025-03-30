mkdir -p audio
alembic upgrade head
python -m uvicorn --host 0.0.0.0 --port 8000 --workers 3 app.main:app