from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers.post import router as post_router
from app.routers.category import router as category_router
from app.routers.location import router as location_router
from app.routers.chatbot import router as chatbot_router

import app.models

BASE_DIR = Path(__file__).resolve().parent
Base.metadata.create_all(bind=engine)

app = FastAPI(title="구미·경북권 여행 정보 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router)
app.include_router(category_router)
app.include_router(location_router)
app.include_router(chatbot_router)

@app.get("/")
def root():
    return {"message": "구미·경북권 여행 정보 API"}

@app.get("/")
def root():
    return RedirectResponse(url="/Front_end.html")

@app.get("/{page_name}.html")
def serve_frontend(page_name: str):
    page_path = BASE_DIR / f"{page_name}.html"
    if page_path.exists():
        return FileResponse(page_path)
    raise HTTPException(status_code=404, detail="페이지를 찾을 수 없습니다.")