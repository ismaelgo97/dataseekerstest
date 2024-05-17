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

def get_connection_by_user(db: Session, user_id: int):
    return db.query(models.Connection).filter(or_(models.Connection.sender_id == user_id, models.Connection.receiver_id == user_id)).all()

def get_connection_by_sender(db: Session, user_id: int):
    return db.query(models.Connection).filter(models.Connection.sender_id == user_id).all()

def get_connection_by_receiver(db: Session, user_id: int):
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
    elif db_connection.answered:
        return True
    elif not db_connection.answered:
        return False
    db_connection.answered = answer
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection

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