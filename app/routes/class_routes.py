from fastapi import APIRouter, HTTPException, Depends
from app.models.class_model import ClassModel
from database import getDB,session
from app.database_models.db_class_model import DBClassModel
from sqlalchemy.orm import Session



router=APIRouter(prefix="/classes", tags=["Classes"])

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
   db=session()
   count = db.query(DBClassModel).count()
   if count ==0:
       for class_item in classList:
           db_class=DBClassModel(
               class_id=class_item.class_id,
               class_name=class_item.class_name
           )
           db.add(db_class)
       db.commit()

initDB()    

@router.get("/all")
def getAllClasses(db: Session = Depends(getDB)):
    classes = db.query(DBClassModel).all()
    if not classes:
        for class_item in classList:
            db_class=DBClassModel(
                class_id=class_item.class_id,
                class_name=class_item.class_name
            )
            db.add(db_class)
        db.commit()
        classes = db.query(DBClassModel).all()
    return classes