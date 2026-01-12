from fastapi import APIRouter, HTTPException, Depends
from database import getDB, session
from app.database_models.db_student_model import DBStudentModel
from sqlalchemy.orm import Session


import matplotlib
matplotlib.use("Agg")  # non-GUI backend (SAFE for FastAPI)
import matplotlib.pyplot as plt
from sqlalchemy import func
from fastapi.responses import StreamingResponse
from io import BytesIO


router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/")
def greet():
    return {"message": "Welcome to the Student Analytics Routes!"}

# get class related student pie chart
@router.get("/class-pie")
def classWiseStudentPieChart(db: Session = Depends(getDB)):

    # 1️.Get class-wise count from DB
    results = (
        db.query(DBStudentModel.class_id, func.count(DBStudentModel.s_id))
        .group_by(DBStudentModel.class_id)
        .all()
    )

    if not results:
        raise HTTPException(status_code=404, detail="No student data found")

    # 2️.Prepare data for chart
    labels = [f"Class {row[0]}" for row in results]
    sizes = [row[1] for row in results]

    # 3️.Create pie chart
    plt.figure()
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Class-wise Student Distribution")
    plt.axis("equal")

    # 4️.Save chart to memory (not disk)
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    # 5️.Return image as response
    return StreamingResponse(buffer, media_type="image/png")
