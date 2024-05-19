from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from . import models, schemas

## Users

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_suggestions_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email.contains(email)).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_users_connections(db: Session, id: str):
    db_connections = get_connections_by_user(db, id)
    db_users = []
    for connection in db_connections:
        if connection.answered:
            if connection.receiver_id == id:
                db_users.append(get_user(db, connection.sender_id))
            else:
                db_users.append(get_user(db, connection.receiver_id))
    return db_users

def get_users_declined_connections(db: Session, id: str):
    db_connections = get_connections_declined_by_user(db, id)
    db_users = []
    for connection in db_connections:
        if connection.answered is False:
            if connection.receiver_id == id:
                db_users.append(get_user(db, connection.sender_id))
            else:
                db_users.append(get_user(db, connection.receiver_id))
    return db_users

def get_users_pending_connections(db: Session, id: str):
    db_connections = get_connections_pending_by_user(db, id)
    db_users = []
    for connection in db_connections:
        if connection.answered is None:
            if connection.receiver_id == id:
                db_users.append(get_user(db, connection.sender_id))
            else:
                db_users.append(get_user(db, connection.receiver_id))
    return db_users

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

## Connections

def get_connection(db: Session, connection_id: int):
    return db.query(models.Connection).filter(models.Connection.id == connection_id).first()

def get_connections_by_user(db: Session, user_id: int):
    return db.query(models.Connection).filter(and_(or_(models.Connection.sender_id == user_id, models.Connection.receiver_id == user_id)), models.Connection.answered == True).all()

def get_connections_received_by_user(db: Session, user_id: int, state: bool | None = True):
    return db.query(models.Connection).filter(and_(models.Connection.receiver_id == user_id), models.Connection.answered == state).all()

def get_connections_sent_by_user(db: Session, user_id: int, state: bool | None = True):
    return db.query(models.Connection).filter(and_(models.Connection.sender_id == user_id), models.Connection.answered == state).all()

def get_connections_declined_by_user(db: Session, user_id: int):
    return db.query(models.Connection).filter(and_(or_(models.Connection.sender_id == user_id, models.Connection.receiver_id == user_id)), models.Connection.answered == False).all()

def get_connections_pending_by_user(db: Session, user_id: int):
    return db.query(models.Connection).filter(and_(or_(models.Connection.sender_id == user_id, models.Connection.receiver_id == user_id)), models.Connection.answered == None).all()

def get_connections_by_sender(db: Session, user_id: int):
    return db.query(models.Connection).filter(models.Connection.sender_id == user_id).all()

def get_connections_by_receiver(db: Session, user_id: int):
    return db.query(models.Connection).filter(models.Connection.receiver_id == user_id).all()

def get_connection_by_users(db: Session, sender_id: int, receiver_id: int):
    return db.query(models.Connection).filter(and_(or_(
        models.Connection.sender_id == sender_id, models.Connection.receiver_id == sender_id),
        or_(models.Connection.sender_id == receiver_id, models.Connection.receiver_id == receiver_id))).first()

def get_connections(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Connection).offset(skip).limit(limit).all()

def answer_connection(db: Session, connection_id: int, answer: bool):
    db_connection = db.query(models.Connection).filter(models.Connection.id == connection_id).first()
    if db_connection is None:
        return None
    elif db_connection.answered is None:
        db_connection.answered = answer
        db.add(db_connection)
        db.commit()
        db.refresh(db_connection)
        return db_connection
    elif db_connection.answered is True:
        return True
    else:
        return False

def create_connection(db: Session, connection: schemas.ConnectionCreate):
    db_connection = models.Connection(sender_id = connection.sender_id, receiver_id = connection.receiver_id)
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection

def delete_connection(db: Session, connection_id: int):
    db_connection = db.query(models.Connection).filter(models.Connection.id == connection_id).first()
    if db_connection is None:
        return None
    db.delete(db_connection)
    db.commit()
    return db_connection