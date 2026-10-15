import os
import time
import uuid

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = os.getenv("APP_EMAIL", "24f2007662@ds.study.iitm.ac.in")
ALLOWED_ORIGIN = "https://dash-1c18d9.example.com"

app = FastAPI(title="CORS Stats API")

# Add CORS first. The request middleware below wraps it, so request headers
# are attached even to CORS preflight responses.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.middleware("http")
async def request_metadata(request: Request, call_next):
    started = time.perf_counter()
    request_id = str(uuid.uuid4())
    try:
        response = await call_next(request)
    except Exception:
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )
    elapsed = max(0.0, time.perf_counter() - started)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response

@app.get("/stats")
async def stats(values: str = Query(..., description="Comma-separated integers")):
    parts = values.split(",")
    try:
        numbers = [int(part.strip()) for part in parts]
    except ValueError:
        raise HTTPException(status_code=400, detail="values must be comma-separated integers")

    if not numbers:
        raise HTTPException(status_code=400, detail="values must contain at least one integer")

    total = sum(numbers)
    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / len(numbers),
    }

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
