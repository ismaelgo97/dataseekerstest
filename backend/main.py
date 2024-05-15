from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, HTTPException
import models
from db import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class User(BaseModel):
    name: str = Field(min_length=1)

USERS = []

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@app.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    user_model = models.Users()
    user_model.name = user.name
    db.add(user_model)
    db.commit()
    return {"message": "User created successfully",
            "user": user}

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Users).get(user_id)

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model == None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id}: Does not exist"
        )
    user_model.name = user.name
    db.add(user_model)
    db.commit()
    return {"message": "User updated successfully",
            "user": user}

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model == None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id}: Does not exist"
        ) 
    db.query(models.Users).filter(models.Users.id == user_id).delete()
    db.commit()
    return {"message": "User deleted successfully",
            "user": user_model}