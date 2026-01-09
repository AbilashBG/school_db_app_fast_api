from fastapi import APIRouter, HTTPException, Depends
from app.models.class_model import ClassModel
from database import getDB, session
from app.database_models.db_class_model import DBClassModel
from sqlalchemy.orm import Session



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