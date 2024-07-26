from .auth import auth_router
from .data_ingest import data_ingest_router
from .monitor import monitor_router
from .predict import predict_router

# Optionally, you could include a function to get all routers at once
def get_routers():
    return [
        auth_router,
        data_ingest_router,
        monitor_router,
        predict_router
    ]

