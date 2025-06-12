from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return {"message": "Welcome to Data API Server"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/data/users")
async def get_users():
    return {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ]
    }

@app.post("/data/users")
async def create_user(user: dict):
    return {"message": "User created", "user": user}

@app.get("/data/stats")
async def get_stats():
    return {
        "total_users": 2,
        "active_sessions": 5,
        "server_uptime": "2 hours"
    }