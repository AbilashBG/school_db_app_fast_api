from fastapi import APIRouter, HTTPException, Depends
from app.models.student_model import StudentModel
from database import getDB, session
from app.database_models.db_student_model import DBStudentModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/")
def greet():
    return {"message": "Welcome to the Student Routes!"}

studentList = [
    StudentModel(s_id=1, name="Alice", class_id=1, dob="2005-06-15", gender="Female", fees_has_paid=True),
    StudentModel(s_id=2, name="Bob", class_id=2, dob="2004-08-22", gender="Male", fees_has_paid=False),
    StudentModel(s_id=3, name="Charlie", class_id=1, dob="2005-03-10", gender="Male", fees_has_paid=True),
    StudentModel(s_id=4, name="Diana", class_id=3, dob="2003-12-05", gender="Female", fees_has_paid=False),
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