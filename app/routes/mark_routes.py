from fastapi import APIRouter, HTTPException, Depends
from database import getDB,session
from sqlalchemy.orm import Session
from app.models.mark_model import MarkModel   
from app.database_models.db_mark_model import DBMarkModel

router = APIRouter(prefix="/marks", tags=["Marks"])

@router.get("/")
def greet():    
    return {"message": "Welcome to the Marks Routes!"}

marksList = [
    MarkModel(s_id=1,subject_id=1,marks=80),
    MarkModel(s_id=1,subject_id=2,marks=78),
    MarkModel(s_id=1,subject_id=3,marks=98),
    MarkModel(s_id=1,subject_id=4,marks=76),
    MarkModel(s_id=1,subject_id=5,marks=100),
]

def initDB():
    db = session()
    count = db.query(DBMarkModel).count()
    
    if count == 0:
        for marks in marksList:
            db_mark = DBMarkModel(
                s_id=marks.s_id,
                subject_id=marks.subject_id,
                marks=marks.marks
            )
            db.add(db_mark)
        db.commit()

initDB()

# get all marks from the database ************************************   
@router.get("/all")
def getAllMarks(db: Session = Depends(getDB)):
    marks = db.query(DBMarkModel).all()
    if not marks:
        for mark in marksList:
            db_mark = DBMarkModel(
                s_id=mark.s_id,
                subject_id=mark.subject_id,
                marks=mark.marks
            )
            db.add(db_mark)
        db.commit()
        marks = db.query(DBMarkModel).all()
    return marks

# get marks by student id and subject id ************************************ 
@router.get("/{s_id}/{subject_id}")
def get_mark(s_id: int, subject_id: int, db: Session = Depends(getDB)):
    mark = db.query(DBMarkModel).filter(
        DBMarkModel.s_id == s_id,
        DBMarkModel.subject_id == subject_id
    ).first()

    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found")

    return mark


# add marks by student id and subject id ************************************ 
@router.post("/")
def add_mark(mark: MarkModel, db: Session = Depends(getDB)):
    existing_mark = db.query(DBMarkModel).filter(
        DBMarkModel.s_id == mark.s_id,
        DBMarkModel.subject_id == mark.subject_id
    ).first()

    if existing_mark:
        raise HTTPException(
            status_code=400,
            detail="Mark already exists for this student and subject"
        )

    db_mark = DBMarkModel(
        s_id=mark.s_id,
        subject_id=mark.subject_id,
        marks=mark.marks
    )

    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)

    return {"message": "Mark added successfully", "data": db_mark}


# update marks by student id and subject id ************************************ 
@router.put("/{s_id}/{subject_id}")
def update_mark(
    s_id: int,
    subject_id: int,
    new_marks: int,
    db: Session = Depends(getDB)
):
    mark = db.query(DBMarkModel).filter(
        DBMarkModel.s_id == s_id,
        DBMarkModel.subject_id == subject_id
    ).first()

    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found")

    mark.marks = new_marks
    db.commit()
    db.refresh(mark)

    return {"message": "Mark updated successfully", "data": mark}


# delete marks by student id and subject id ************************************ 
@router.delete("/{s_id}/{subject_id}")
def delete_mark(s_id: int, subject_id: int, db: Session = Depends(getDB)):
    mark = db.query(DBMarkModel).filter(
        DBMarkModel.s_id == s_id,
        DBMarkModel.subject_id == subject_id
    ).first()

    if not mark:
        raise HTTPException(status_code=404, detail="Mark not found")

    db.delete(mark)
    db.commit()

    return {"message": "Mark deleted successfully"}
