from fastapi import APIRouter, HTTPException, Depends
from database import getDB,session
from sqlalchemy.orm import Session
from app.models.teacher_model import TeacherModel   
from app.database_models.db_teacher_model import DBTeacherModel

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.get("/")
def greet():    
    return {"message": "Welcome to the Teacher Routes!"}

teacherList = [
    TeacherModel(t_id=1, name="Mr. Smith", subject="Tamil", class_id=1, salary=50000.00),
    TeacherModel(t_id=2, name="Ms. Johnson", subject="English", class_id=2, salary=52000.00),
    TeacherModel(t_id=3, name="Mrs. Brown", subject="Maths", class_id=1, salary=51000.00),
    TeacherModel(t_id=4, name="Mr. Davis", subject="Science", class_id=3, salary=53000.00),
]

def initDB():
    db = session()
    count = db.query(DBTeacherModel).count()
    
    if count == 0:
        for teacher in teacherList:
            db_teacher = DBTeacherModel(
                t_id=teacher.t_id,
                name=teacher.name,
                subject=teacher.subject,
                class_id=teacher.class_id,
                salary=teacher.salary
            )
            db.add(db_teacher)
        db.commit()

initDB()


# get all teachers from the database ************************************   
@router.get("/all")
def getAllTeachers(db: Session = Depends(getDB)):
    teachers = db.query(DBTeacherModel).all()
    if not teachers:
        for teacher in teacherList:
            db_teacher = DBTeacherModel(
                t_id=teacher.t_id,
                name=teacher.name,
                subject=teacher.subject,
                class_id=teacher.class_id,
                salary=teacher.salary
            )
            db.add(db_teacher)
        db.commit()
        teachers = db.query(DBTeacherModel).all()
    return teachers

# get teacher by id ******************************************************
@router.get("/{t_id}")
def getTeacherById(t_id: int, db: Session = Depends(getDB)):
    teacher = db.query(DBTeacherModel).filter(DBTeacherModel.t_id == t_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

# add a new teacher ******************************************************
@router.post("/add")
def addTeacher(teacher: TeacherModel, db: Session = Depends(getDB)):    

     if db.query(DBTeacherModel).filter(DBTeacherModel.t_id == teacher.t_id).first():
        raise HTTPException(status_code=400, detail="Teacher with this ID already exists")   
     
     db_teacher = DBTeacherModel(
         t_id=teacher.t_id,
         name=teacher.name,
         subject=teacher.subject,
         class_id=teacher.class_id,
         salary=teacher.salary   
     )
     db.add(db_teacher)
     db.commit()
     db.refresh(db_teacher)
     return db_teacher


# get teachers by class id ************************************************
@router.get("/class/{class_id}")
def getTeachersByClassId(class_id: int, db: Session = Depends(getDB)):  
    teachers = db.query(DBTeacherModel).filter(DBTeacherModel.class_id == class_id).all()
    if teachers:
        return teachers
    raise HTTPException(status_code=404, detail="No teachers found for the given class ID")

# get teachers by subject ************************************************
@router.get("/subject/{subject}")
def getTeachersBySubject(subject: str, db: Session = Depends(getDB)):   
    teachers = db.query(DBTeacherModel).filter(DBTeacherModel.subject == subject).all()
    if teachers:
        return teachers
    raise HTTPException(status_code=404, detail="No teachers found for the given subject")


# update teacher details ************************************************
@router.put("/update/{t_id}")
def updateTeacher(t_id: int, teacher: TeacherModel, db: Session = Depends(getDB)):
    db_teacher = db.query(DBTeacherModel).filter(DBTeacherModel.t_id == t_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    db_teacher.name = teacher.name
    db_teacher.subject = teacher.subject
    db_teacher.class_id = teacher.class_id
    db_teacher.salary = teacher.salary
    
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

# delete teacher by id **************************************************
@router.delete("/delete/{t_id}")    
def deleteTeacherById(t_id: int, db: Session = Depends(getDB)):  
    teacher = db.query(DBTeacherModel).filter(DBTeacherModel.t_id == t_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted successfully"}


# delete teachers by class id *******************************************
@router.delete("/delete/class/{class_id}")
def deleteTeachersByClassId(class_id: int, db: Session = Depends(getDB)):
    teachers = db.query(DBTeacherModel).filter(DBTeacherModel.class_id == class_id).all()
    if not teachers:
        raise HTTPException(status_code=404, detail="No teachers found for the given class ID")
    for teacher in teachers:
        db.delete(teacher)
    db.commit()
    return {"message": "Teachers deleted successfully"}

# delete teachers by subject *********************************************
@router.delete("/delete/subject/{subject}")
def deleteTeachersBySubject(subject: str, db: Session = Depends(getDB)):
    teachers = db.query(DBTeacherModel).filter(DBTeacherModel.subject == subject).all()
    if not teachers:
        raise HTTPException(status_code=404, detail="No teachers found for the given subject")
    for teacher in teachers:
        db.delete(teacher)
    db.commit()
    return {"message": "Teachers deleted successfully"}

# update teacher salary by id *******************************************
@router.put("/update/salary/{t_id}")
def updateTeacherSalary(t_id: int, salary: float, db: Session = Depends(getDB)):
    db_teacher = db.query(DBTeacherModel).filter(DBTeacherModel.t_id == t_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db_teacher.salary = salary
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

