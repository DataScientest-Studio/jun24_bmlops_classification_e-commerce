from fastapi import FastAPI
from routers import auth, data_ingest, monitor, predict

app = FastAPI()

app.include_router(auth.router)
app.include_router(data_ingest.router)
app.include_router(monitor.router)
app.include_router(predict.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
