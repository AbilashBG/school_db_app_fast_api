from fastapi import APIRouter, HTTPException, Depends
from app.models.student_model import StudentModel,GenderEnum
from database import getDB, session
from app.database_models.db_student_model import DBStudentModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/")
def greet():
    return {"message": "Welcome to the Student Routes!"}

studentList = [

    # -------- Class 1 (5 students) --------
    StudentModel(s_id=1, name="Alice", class_id=1, dob="2005-01-10", gender=GenderEnum.Female, fees_has_paid=True),
    StudentModel(s_id=2, name="Bob", class_id=1, dob="2005-02-12", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=3, name="Cathy", class_id=1, dob="2005-03-14", gender=GenderEnum.Female, fees_has_paid=False),
    StudentModel(s_id=4, name="David", class_id=1, dob="2005-04-16", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=5, name="Eva", class_id=1, dob="2005-05-18", gender=GenderEnum.Female, fees_has_paid=False),

    # -------- Class 2 (15 students) --------
    StudentModel(s_id=6, name="Frank", class_id=2, dob="2004-01-11", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=7, name="Grace", class_id=2, dob="2004-02-13", gender=GenderEnum.Female, fees_has_paid=True),
    StudentModel(s_id=8, name="Henry", class_id=2, dob="2004-03-15", gender=GenderEnum.Male, fees_has_paid=False),
    StudentModel(s_id=9, name="Irene", class_id=2, dob="2004-04-17", gender=GenderEnum.Female, fees_has_paid=True),
    StudentModel(s_id=10, name="Jack", class_id=2, dob="2004-05-19", gender=GenderEnum.Male, fees_has_paid=False),
    StudentModel(s_id=11, name="Karen", class_id=2, dob="2004-06-21", gender=GenderEnum.Female, fees_has_paid=True),
    StudentModel(s_id=12, name="Leo", class_id=2, dob="2004-07-23", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=13, name="Mona", class_id=2, dob="2004-08-25", gender=GenderEnum.Female, fees_has_paid=False),
    StudentModel(s_id=14, name="Nick", class_id=2, dob="2004-09-27", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=15, name="Olivia", class_id=2, dob="2004-10-29", gender=GenderEnum.Female, fees_has_paid=True),
    StudentModel(s_id=16, name="Paul", class_id=2, dob="2004-11-05", gender=GenderEnum.Male, fees_has_paid=False),
    StudentModel(s_id=17, name="Queen", class_id=2, dob="2004-12-07", gender=GenderEnum.Female, fees_has_paid=True),
    StudentModel(s_id=18, name="Ryan", class_id=2, dob="2004-01-09", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=19, name="Sophia", class_id=2, dob="2004-02-11", gender=GenderEnum.Female, fees_has_paid=False),
    StudentModel(s_id=20, name="Tom", class_id=2, dob="2004-03-13", gender=GenderEnum.Male, fees_has_paid=True),

    # -------- Class 3 (12 students) --------
    StudentModel(s_id=21, name="Uma", class_id=3, dob="2003-01-14", gender=GenderEnum.Female, fees_has_paid=True),
    StudentModel(s_id=22, name="Victor", class_id=3, dob="2003-02-16", gender=GenderEnum.Male, fees_has_paid=False),
    StudentModel(s_id=23, name="Wendy", class_id=3, dob="2003-03-18", gender=GenderEnum.Female, fees_has_paid=True),
    StudentModel(s_id=24, name="Xavier", class_id=3, dob="2003-04-20", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=25, name="Yara", class_id=3, dob="2003-05-22", gender=GenderEnum.Female, fees_has_paid=False),
    StudentModel(s_id=26, name="Zack", class_id=3, dob="2003-06-24", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=27, name="Alan", class_id=3, dob="2003-07-26", gender=GenderEnum.Male, fees_has_paid=False),
    StudentModel(s_id=28, name="Bella", class_id=3, dob="2003-08-28", gender=GenderEnum.Female, fees_has_paid=True),
    StudentModel(s_id=29, name="Chris", class_id=3, dob="2003-09-30", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=30, name="Daisy", class_id=3, dob="2003-10-02", gender=GenderEnum.Female, fees_has_paid=False),
    StudentModel(s_id=31, name="Ethan", class_id=3, dob="2003-11-04", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=32, name="Fiona", class_id=3, dob="2003-12-06", gender=GenderEnum.Female, fees_has_paid=True),

    # -------- Class 4 (8 students) --------
    StudentModel(s_id=33, name="George", class_id=4, dob="2002-01-08", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=34, name="Hannah", class_id=4, dob="2002-02-10", gender=GenderEnum.Female, fees_has_paid=False),
    StudentModel(s_id=35, name="Ian", class_id=4, dob="2002-03-12", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=36, name="Julia", class_id=4, dob="2002-04-14", gender=GenderEnum.Female, fees_has_paid=True),
    StudentModel(s_id=37, name="Kevin", class_id=4, dob="2002-05-16", gender=GenderEnum.Male, fees_has_paid=False),
    StudentModel(s_id=38, name="Lily", class_id=4, dob="2002-06-18", gender=GenderEnum.Female, fees_has_paid=True),
    StudentModel(s_id=39, name="Mark", class_id=4, dob="2002-07-20", gender=GenderEnum.Male, fees_has_paid=True),
    StudentModel(s_id=40, name="Nina", class_id=4, dob="2002-08-22", gender=GenderEnum.Female, fees_has_paid=False),
]


def initDB():
    db = session()
    count = db.query(DBStudentModel).count()
    
    if count == 0:
        for student in studentList:
            db_student = DBStudentModel(
                s_id=student.s_id,
                name=student.name,
                class_id=student.class_id,
                dob=student.dob,
                gender=student.gender,
                fees_has_paid=student.fees_has_paid
            )
            db.add(db_student)
        db.commit()

initDB()    

# get all students from the database ************************************

@router.get("/all")
def getAllStudents(db: Session = Depends(getDB)):
    students = db.query(DBStudentModel).all()
    if not students:
        for student in studentList:
            db_student = DBStudentModel(
                s_id=student.s_id,
                name=student.name,
                class_id=student.class_id,
                dob=student.dob,
                gender=student.gender,
                fees_has_paid=student.fees_has_paid
            )
            db.add(db_student)
        db.commit()
        students = db.query(DBStudentModel).all()
    return students

# get student by id ******************************************************
@router.get("/{s_id}")
def getStudentById(s_id: int, db: Session = Depends(getDB)):
    student = db.query(DBStudentModel).filter(DBStudentModel.s_id == s_id).first()
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found")

# get students by class id ************************************************
@router.get("/class/{class_id}")
def getStudentsByClassId(class_id: int, db: Session = Depends(getDB)):
    students = db.query(DBStudentModel).filter(DBStudentModel.class_id == class_id).all()
    if students:
        return students
    raise HTTPException(status_code=404, detail="No students found for the given class ID")

# get students by gender ************************************************
@router.get("/gender/{gender}")
def getStudentsByGender(gender: str, db: Session = Depends(getDB)):
    students = db.query(DBStudentModel).filter(DBStudentModel.gender == gender).all()
    if students:
        return students     
    raise HTTPException(status_code=404, detail="No students found for the given gender")

# add new student *******************************************************       
@router.post("/add")
def addStudent(student: StudentModel, db: Session = Depends(getDB)):

    if db.query(DBStudentModel).filter(DBStudentModel.s_id == student.s_id).first():
        raise HTTPException(status_code=400, detail="Student with this ID already exists")   
    
    db_student = DBStudentModel(
        s_id=student.s_id,
        name=student.name,
        class_id=student.class_id,
        dob=student.dob,    
        gender=student.gender,
        fees_has_paid=student.fees_has_paid 
    )
    db.add(db_student)
    db.commit()
    return {"message": "Student added successfully", "student": db_student}

# delete student by id **************************************************
@router.delete("/delete/{s_id}")    
def deleteStudentById(s_id: int, db: Session = Depends(getDB)):
    student = db.query(DBStudentModel).filter(DBStudentModel.s_id == s_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

# delete students by class id *******************************************
@router.delete("/delete/class/{class_id}")    
def deleteStudentsByClassId(class_id: int, db: Session = Depends(getDB)):
    students = db.query(DBStudentModel).filter(DBStudentModel.class_id == class_id).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for the given class ID")
    for student in students:
        db.delete(student)
    db.commit()
    return {"message": "Students deleted successfully"}

# delete students by gender ***********************************************
@router.delete("/delete/gender/{gender}")    
def deleteStudentsByGender(gender: str, db: Session = Depends(getDB)):
    students = db.query(DBStudentModel).filter(DBStudentModel.gender == gender).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for the given gender")
    for student in students:
        db.delete(student)
    db.commit()
    return {"message": "Students deleted successfully"}

# update student by id **************************************************
@router.put("/update/{s_id}")
def updateStudentById(s_id: int, student: StudentModel, db: Session =Depends(getDB)):
    db_student = db.query(DBStudentModel).filter(DBStudentModel.s_id == s_id).first()
    if db_student:
        db_student.name = student.name
        db_student.class_id = student.class_id
        db_student.dob = student.dob
        db_student.gender = student.gender
        db_student.fees_has_paid = student.fees_has_paid
        db.commit()
        return {"message": "Student updated successfully", "student": db_student}
    raise HTTPException(status_code=404, detail="Student not found")

# get students by fees status ********************************************
@router.get("/fees/pending")
def getPendingFeesStudents(db: Session = Depends(getDB)):
    students = db.query(DBStudentModel).filter(DBStudentModel.fees_has_paid == False).all()
    if students:
        return students
    raise HTTPException(status_code=404, detail="No students with pending fees found")

# get students by fees status ********************************************
@router.get("/fees/paid")
def getPaidFeesStudents(db: Session = Depends(getDB)):  
    students = db.query(DBStudentModel).filter(DBStudentModel.fees_has_paid == True).all()
    if students:
        return students
    raise HTTPException(status_code=404, detail="No students with paid fees found")

# update student fees status ********************************************
@router.put("/fees/update/{s_id}")
def updateStudentFeesStatus(s_id: int, fees_has_paid: bool, db: Session = Depends(getDB)):
    db_student = db.query(DBStudentModel).filter(DBStudentModel.s_id == s_id).first()
    if db_student:
        db_student.fees_has_paid = fees_has_paid
        db.commit()
        return {"message": "Student fees status updated successfully", "student": db_student}
    raise HTTPException(status_code=404, detail="Student not found")

# get students by gender and class id **************************************
@router.get("/studentsByGenderAndClass/{gender}/{class_id}")
def getStudentsByGenderAndClass(gender: str, class_id: int, db: Session = Depends(getDB)):
    students = db.query(DBStudentModel).filter(DBStudentModel.gender == gender, DBStudentModel.class_id == class_id).all()
    if students:
        return students 
    raise HTTPException(status_code=404, detail="No students found for the given gender and class ID")