from fastapi import FastAPI, Depends, HTTPException
from db_app import models
from db_app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from db_app import crud, models, schemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

## Users
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@app.get("/users/email/{email}", response_model=schemas.User)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user

@app.get("/users/suggest/{email}", response_model=list[schemas.User])
def suggest_users_by_email(email: str, db: Session = Depends(get_db)):
    db_users = crud.get_user_suggestions_by_email(db, email)
    if db_users is None:
        raise HTTPException(status_code=400, detail="Not users found")
    return db_users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/connections/{user_id}", response_model=list[schemas.User])
def get_users_connections_by_state(user_id: int, state: bool | None = True, db: Session = Depends(get_db)):
    db_users = None
    if state is True:
        db_users = crud.get_users_connections(db, user_id)
    elif state is False:
        db_users = crud.get_users_declined_connections(db, user_id)
    else:
        db_users = crud.get_users_pending_connections(db, user_id)
    return db_users

## Connections
@app.get("/connections/", response_model=list[schemas.Connection])
def read_connections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    connections = crud.get_connections(db, skip, limit)
    return connections

@app.get("/connections/{connection_id}", response_model=schemas.Connection)
def read_connection(connection_id: int, db: Session = Depends(get_db)):
    db_connection = crud.get_connection(db, connection_id)
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    return db_connection

@app.get("/connections/user/{user_id}", response_model=list[schemas.Connection])
def read_connections_by_user(user_id: int, db: Session = Depends(get_db)):
    db_connections = crud.get_connection_by_user(db, user_id)
    if db_connections is None:
        raise HTTPException(status_code=404, detail="Connections not found")
    return db_connections

@app.post("/connections/", response_model=schemas.Connection)
def create_connection(connection: schemas.ConnectionCreate, db: Session = Depends(get_db)):
    db_sender = crud.get_user(db, connection.sender_id)
    db_receiver = crud.get_user(db, connection.receiver_id)
    if db_sender is None and db_receiver is None:
        raise HTTPException(status_code=400, detail="Users not found")
    elif db_sender is None:
        raise HTTPException(status_code=400, detail="Sender not found")
    elif db_receiver is None:
        raise HTTPException(status_code=400, detail="Receiver not found")
    db_connection = crud.get_connection_by_users(db, connection.sender_id, connection.receiver_id)
    if db_connection is None:
        return crud.create_connection(db, connection)
    elif db_connection.receiver_id == connection.sender_id:
        return crud.answer_connection(db, db_connection.id, True)
    raise HTTPException(status_code=400, detail="Connection already requested") 

@app.delete("/connections/{connection_id}", response_model=schemas.Connection)
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    db_connection = crud.delete_connection(db, connection_id)
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    return db_connection

@app.put("/connections/answer/{connection_id}", response_model=schemas.Connection)
def answer_connection(connection_id: int, answer: bool, db: Session = Depends(get_db)):
    db_connection = crud.answer_connection(db, connection_id, answer)
    if db_connection is None:
        raise HTTPException(status_code=400, detail="Connection not found")
    elif db_connection is True:
        raise HTTPException(status_code=400, detail="Connection already accepted")
    elif db_connection is False:
        raise HTTPException(status_code=400, detail="Connection already declined")
    return db_connection