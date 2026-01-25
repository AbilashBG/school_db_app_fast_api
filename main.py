from fastapi import FastAPI
from database import Base, engine

# Import all database models BEFORE creating tables
from app.database_models.db_class_model import DBClassModel
from app.database_models.db_student_model import DBStudentModel
from app.database_models.db_teacher_model import DBTeacherModel
from app.database_models.db_subject_model import DBSubjectModel
from app.database_models.db_mark_model import DBMarkModel

app = FastAPI()

# Create tables after models are imported
Base.metadata.create_all(bind=engine)

# Import routes after tables are created
from app.routes.class_routes import router as class_router
from app.routes.student_routes import router as student_router
from app.routes.teacher_routes import router as teacher_router
from app.routes.subject_routes import router as subject_routes
from app.routes.mark_routes import router as mark_router
from app.routes.student_analytics_routes import router as analytics_router
from app.routes.login_routes import router as login_router

@app.get("/")
def greet():
    return {"message": "Welcome to the School Database API!"}

app.include_router(login_router)
app.include_router(class_router)
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(subject_routes)
app.include_router(mark_router)
app.include_router(analytics_router)


