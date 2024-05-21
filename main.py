from fastapi import FastAPI
from app.routers import router
from app.database import engine, Base

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
