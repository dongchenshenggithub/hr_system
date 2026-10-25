from fastapi import FastAPI

from app.core.database import Base, engine
from app.features.employees.router import router as employees_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HR System")

app.include_router(employees_router)


@app.get("/health")
def health():
    return {"status": "ok"}
