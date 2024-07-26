from fastapi import APIRouter

router = APIRouter()


@router.get("/api/monitor")
async def monitor():
    return {"message": "Monitoring"}
