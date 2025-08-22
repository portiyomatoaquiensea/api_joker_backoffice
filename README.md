
Set Environment Variables in Railway

Go to Settings → Environment Variables

Add all keys from your .env.

Configure Start Command
Railway needs to know how to run FastAPI:

uvicorn app.main:app --host 0.0.0.0 --port $PORT