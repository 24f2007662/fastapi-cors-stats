# FastAPI CORS Stats API

## Local run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Test
```bash
curl -i 'http://localhost:8000/stats?values=1,2,3,4'
curl -i -X OPTIONS 'http://localhost:8000/stats' \
  -H 'Origin: https://dash-1c18d9.example.com' \
  -H 'Access-Control-Request-Method: GET'
curl -i -X OPTIONS 'http://localhost:8000/stats' \
  -H 'Origin: https://evil.example' \
  -H 'Access-Control-Request-Method: GET'
```

Allowed-origin preflight should include `Access-Control-Allow-Origin: https://dash-1c18d9.example.com`.
The evil-origin preflight should not include `Access-Control-Allow-Origin`.

## Deploy on Render
1. Create a GitHub repository and upload these project files.
2. In Render, choose **New + → Blueprint**, connect the repository, and deploy.
3. Copy the generated `https://....onrender.com` base URL and test `/healthz` and `/stats`.
