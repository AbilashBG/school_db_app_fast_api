from fastapi import FastAPI
from database import Base, engine

# Import all database models BEFORE creating tables
from app.database_models.db_class_model import DBClassModel
from app.database_models.db_student_model import DBStudentModel

app = FastAPI()

# Create tables after models are imported
Base.metadata.create_all(bind=engine)

# Import routes after tables are created
from app.routes.class_routes import router as class_router
from app.routes.student_routes import router as student_router

@app.get("/")
def greet():
    return {"message": "Welcome to the School Database API!"}

app.include_router(class_router)
app.include_router(student_router)

