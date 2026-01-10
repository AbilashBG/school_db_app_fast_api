from fastapi import APIRouter, HTTPException, Depends,Query
from app.models.class_model import ClassModel
from database import getDB, session
from app.database_models.db_class_model import DBClassModel
from app.database_models.db_student_model import DBStudentModel
from app.database_models.db_teacher_model import DBTeacherModel
from sqlalchemy.orm import Session
from app.models.class_detail_model import ClassDetailResponse



router = APIRouter(prefix="/classes", tags=["Classes"])

@router.get("/")
def greet():
    return {"message": "Welcome to the Class Routes!"}

classList = [
    ClassModel(class_id=1, class_name="10-A"),
    ClassModel(class_id=2, class_name="10-B"),  
    ClassModel(class_id=3, class_name="11-A"),  
    ClassModel(class_id=4, class_name="11-B"),
]

def initDB():
    db = session()
    count = db.query(DBClassModel).count()
    if count == 0:
        for class_item in classList:
            db_class = DBClassModel(
                class_id=class_item.class_id,
                class_name=class_item.class_name
            )
            db.add(db_class)
        db.commit()

initDB()    

# get all classes from the database ************************************

@router.get("/all")
def getAllClasses(db: Session = Depends(getDB)):
    classes = db.query(DBClassModel).all()
    if not classes:
        for class_item in classList:
            db_class = DBClassModel(
                class_id=class_item.class_id,
                class_name=class_item.class_name
            )
            db.add(db_class)
        db.commit()
        classes = db.query(DBClassModel).all()
    return classes


# get class by id ******************************************************

@router.get("/{class_id}")
def getClassById(class_id: int,db:Session=Depends(getDB)):
    class_item=db.query(DBClassModel).filter(DBClassModel.class_id==class_id).first()
    if class_item:
        return class_item
    raise HTTPException(status_code=404, detail="Class not found") 

# get class by name ****************************************************

@router.get("/name/{class_name}")
def getClassByName(class_name: str, db: Session = Depends(getDB)):
    class_item = db.query(DBClassModel).filter(DBClassModel.class_name == class_name).first()
    if class_item:
        return class_item       
    raise HTTPException(status_code=404, detail="Class not found")
    

# add new class ******************************************************* 

@router.post("/add")
def addClass(class_item: ClassModel, db: Session = Depends(getDB)):

    if db.query(DBClassModel).filter(DBClassModel.class_id == class_item.class_id).first():
        raise HTTPException(status_code=400, detail="Class with this ID already exists")   

    if db.query(DBClassModel).filter(DBClassModel.class_name == class_item.class_name).first():
        raise HTTPException(status_code=400, detail="Class with this name already exists")   
    
    db_class = DBClassModel(
        class_id=class_item.class_id,
        class_name=class_item.class_name
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return {"message": "Class added successfully", "class": db_class}    

# delete class by id **************************************************

@router.delete("/delete/{class_id}")
def deleteClassById(class_id: int, db: Session = Depends(getDB)):
    class_item = db.query(DBClassModel).filter(DBClassModel.class_id == class_id).first()
    if not class_item:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(class_item)
    db.commit()
    return {"message": "Class deleted successfully"}

# update class by id ************************************************** 
@router.put("/update/{class_id}")
def updateClassById(class_id: int, updated_class: ClassModel, db: Session = Depends(getDB)):
    class_item = db.query(DBClassModel).filter(DBClassModel.class_id == class_id).first()
    if not class_item:
        raise HTTPException(status_code=404, detail="Class not found")
    
    class_item.class_name = updated_class.class_name
    db.commit()
    db.refresh(class_item)
    return {"message": "Class updated successfully", "class": class_item}



# get class details *********************************************************************
# You are telling FastAPI: “Whatever I return from this API, convert it into this Pydantic model (ClassDetailResponse) before sending to client.”


@router.get("/classDetails/{class_id}", response_model=ClassDetailResponse)
def get_class_details(
    class_id: int,
    #Query Used for query parameters (?page=1&limit=10) Allows validation (greater than or eql, lessthan or eql)
    student_page: int = Query(1, ge=1), 
    student_limit: int = Query(10, le=100),
    teacher_page: int = Query(1, ge=1),
    teacher_limit: int = Query(10, le=100),
    # Depends means dependency injection which is used for inject DB Session
    db: Session = Depends(getDB)
):
    # ---- Fetch Class ----
    class_obj = db.query(DBClassModel).filter(
        DBClassModel.class_id == class_id
    ).first()

    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")

    # ---- Students Pagination ----
    student_query = db.query(DBStudentModel).filter(
        DBStudentModel.class_id == class_id
    )

    total_students = student_query.count()

    # offset = (1 - 1) × 10 = 0  => OFFSET 0
    # Skip nothing, Start from first row  => same like next next pages and count
    students = (
        student_query
        .offset((student_page - 1) * student_limit)
        .limit(student_limit)
        .all()
    )

    # ---- Teachers Pagination ----
    teacher_query = db.query(DBTeacherModel).filter(
        DBTeacherModel.class_id == class_id
    )

    total_teachers = teacher_query.count()

    # offset = (1 - 1) × 10 = 0  => OFFSET 0
    # Skip nothing, Start from first row  => same like next next pages and count
    teachers = (
        teacher_query
        .offset((teacher_page - 1) * teacher_limit)
        .limit(teacher_limit)
        .all()
    )

    return {
        "class_id": class_obj.class_id,
        "class_name": class_obj.class_name,
        "students": {
            "total": total_students,
            "page": student_page,
            "limit": student_limit,
            "data": students
        },
        "teachers": {
            "total": total_teachers,
            "page": teacher_page,
            "limit": teacher_limit,
            "data": teachers
        }
    }