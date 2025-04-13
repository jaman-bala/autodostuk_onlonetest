import sys
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager
from src.api.auth import router as router_auth
from src.api.images import router as router_images
from src.api.questions import router as router_questions
from src.api.tickets import router as router_tickets
from src.api.answers import router as router_answers
from src.api.group import router as router_group
from src.api.payments import router as router_payments
from src.api.reports import router as router_reports
from src.api.themes import router as router_themes
from src.api.totals import router as router_totals
from src.config import settings

app_name = settings.PROJECT_NAME

# Метрики Prometheus
registry = CollectorRegistry()

REQUEST_COUNT = Counter(
    "fastapi_requests_total", "Total HTTP Requests",
    ["method", "endpoint", "http_status", "app_name"],
    registry=registry
)

REQUEST_LATENCY = Histogram(
    "fastapi_request_duration_seconds", "HTTP request latency",
    ["method", "endpoint", "app_name"],
    registry=registry
)

# Redis-кеш
@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager), prefix="fastapi-cache")
    yield
    await redis_manager.close()

app = FastAPI(
    lifespan=lifespan,
    docs=None,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# Middleware для сбора метрик
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path

    with REQUEST_LATENCY.labels(method=method, endpoint=endpoint, app_name=app_name).time():
        response = await call_next(request)

    status_code = response.status_code
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code, app_name=app_name).inc()

    return response

# Ручка для Prometheus
@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)


# Подключение статики
app.mount("/static/avatars", StaticFiles(directory=settings.LINK_IMAGES), name="avatars")
app.mount("/static/photo", StaticFiles(directory=settings.LINK_UPLOAD_PHOTO), name="photo")
app.mount("/static/upload-files", StaticFiles(directory=settings.LINK_UPLOAD_FILES), name="upload-files")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(router_auth)
app.include_router(router_images)
app.include_router(router_tickets)
app.include_router(router_questions)
app.include_router(router_answers)
app.include_router(router_group)
app.include_router(router_payments)
app.include_router(router_reports)
app.include_router(router_themes)
app.include_router(router_totals)

@app.get("/", response_class=JSONResponse)
async def read_root():
    return {"message": "backend 🏆"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
