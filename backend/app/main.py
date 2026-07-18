from fastapi import FastAPI

from backend.app.db.session import Base, engine
from backend.app.models import module2_models
from backend.app.routes.module2_routes import router as module2_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MACE Module 2 API",
    version="1.0.0",
)

app.include_router(module2_router)


@app.get("/")
def root():
    return {"message": "MACE Module 2 API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}