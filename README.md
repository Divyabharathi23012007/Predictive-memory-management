To run:

From the backend directory:
```bash
cd backend
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Or from the root directory:
```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```