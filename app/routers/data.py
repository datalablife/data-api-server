from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/data", tags=["data"])

@router.get("/users")
async def get_users():
    return {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ]
    }

@router.post("/users")
async def create_user(user: Dict[str, Any]):
    return {"message": "User created", "user": user}

@router.get("/stats")
async def get_stats():
    return {
        "total_users": 2,
        "active_sessions": 5,
        "server_uptime": "2 hours"
    }