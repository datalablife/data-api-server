from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import data

app = FastAPI(
    title="Data API Server",
    description="A Python backend API server",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Data API Server"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}