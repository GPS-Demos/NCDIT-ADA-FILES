# Backend Environment Configuration

## Environment Switching

To switch between local and Cloud Run backend, edit `frontend/src/config/backend.ts`:

```typescript
export const BACKEND_CONFIG = {
  // Set to 'local' or 'cloudrun'
  environment: 'local',

  endpoints: {
    local: 'http://localhost:8080',
    cloudrun: 'https://scitility-backend-XXXXX.run.app'
  }
};
```

## Testing Local Python Server

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Deploying to Cloud Run

```bash
cd backend
gcloud run deploy scitility-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Required Environment Variables

See `.env.example` files in both `frontend/` and `backend/` directories.
