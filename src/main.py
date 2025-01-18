import sys
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

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


app.mount("/static/avatars", StaticFiles(directory=settings.LINK_IMAGES), name="avatars")
app.mount("/static/photo", StaticFiles(directory=settings.LINK_UPLOAD_PHOTO), name="photo")
app.mount(
    "/static/upload-files", StaticFiles(directory=settings.LINK_UPLOAD_FILES), name="upload-files"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

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
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)  # host="0.0.0.0",
