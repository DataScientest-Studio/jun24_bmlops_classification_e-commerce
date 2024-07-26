from fastapi import APIRouter

router = APIRouter()


@router.post("/api/data-ingest")
async def data_ingest():
    return {"message": "Data ingested"}
