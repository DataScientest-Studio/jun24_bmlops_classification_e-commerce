from fastapi import APIRouter

router = APIRouter()

@router.post("/api/predict")
async def predict():
    return {"message": "Prediction"}

