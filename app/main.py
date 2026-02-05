from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Diagram Reader")

app.include_router(router)
