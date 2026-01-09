from fastapi import FastAPI
from app.routes.class_routes import router as class_router
from app.database_models.db_class_model import Base
from database import engine

app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(class_router)

