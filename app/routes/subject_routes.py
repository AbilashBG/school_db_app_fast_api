from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from database import getDB, session
from app.models.subject_model import SubjectModel
from app.database_models.db_subject_model import DBSubjectModel

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("/")
def greet():
    return {"message": "Welcome to the Subject Routes!"}


# Static initial data
subjectList = [
    SubjectModel(subject_id=1, subject_name="Tamil"),
    SubjectModel(subject_id=2, subject_name="English"),
    SubjectModel(subject_id=3, subject_name="Maths"),
    SubjectModel(subject_id=4, subject_name="Science"),
    SubjectModel(subject_id=5, subject_name="Social Science"),
]


# Initialize DB (run once)
def initDB():
    db = session()
    try:
        if db.query(DBSubjectModel).count() == 0:
            for subject in subjectList:
                db_subject = DBSubjectModel(
                    subject_id=subject.subject_id,
                    subject_name=subject.subject_name
                )
                db.add(db_subject)
            db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


initDB()

# get all subjects from the database ************************************  
@router.get("/all")
def get_all_subjects(db: Session = Depends(getDB)):
    subjects = db.query(DBSubjectModel).all()
    if not subjects:
        for subject in subjectList:
            db_subject = DBSubjectModel(
                subject_id=subject.subject_id,
                subject_name=subject.subject_name
            )
            db.add(db_subject)
        db.commit()
        subjects = db.query(DBSubjectModel).all()
    return subjects


# get subject by id ******************************************************
@router.get("/{sub_id}")
def getSubjectById(sub_id: int, db: Session = Depends(getDB)):
    subject = db.query(DBSubjectModel).filter(DBSubjectModel.subject_id == sub_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return subject

# add a new subject ******************************************************
@router.post("/add")
def addSubject(newSubject: SubjectModel, db: Session = Depends(getDB)):    

     if db.query(DBSubjectModel).filter(DBSubjectModel.subject_id == newSubject.subject_id).first():
        raise HTTPException(status_code=400, detail="Subject with this ID already exists")   
     
     db_subject = DBSubjectModel(
         subject_id=newSubject.subject_id,
         subject_name=newSubject.subject_name 
     )
     db.add(db_subject)
     db.commit()
     db.refresh(db_subject)
     return {"message":"New Subject added successfully","subject":db_subject}

# update subject details ************************************************
@router.put("/update/{sub_id}")
def updateSubject(sub_id: int, subject: SubjectModel, db: Session = Depends(getDB)):
    db_subject = db.query(DBSubjectModel).filter(DBSubjectModel.subject_id == sub_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    db_subject.subject_id = sub_id
    db_subject.subject_name = subject.subject_name
    
    db.commit()
    db.refresh(db_subject)
    return db_subject

# delete subject by id **************************************************
@router.delete("/delete/{sub_id}")    
def deleteTeacherById(sub_id: int, db: Session = Depends(getDB)):  
    subject = db.query(DBSubjectModel).filter(DBSubjectModel.subject_id == sub_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(subject)
    db.commit()
    return {"message": "Subject deleted successfully"}