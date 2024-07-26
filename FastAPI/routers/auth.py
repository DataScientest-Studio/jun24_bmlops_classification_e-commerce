from fastapi import APIRouter

router = APIRouter()


@router.post("/api/auth")
async def authenticate():
    return {"message": "Authentication"}
