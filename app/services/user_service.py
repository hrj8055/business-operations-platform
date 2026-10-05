from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app import crud, schemas, security


def register_user(db: Session, user: schemas.UserCreate):
    try:
        return crud.create_user(db, user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already registered")


def login_user(db: Session, username: str, password: str):
    user = crud.authenticate_user(db, username, password)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
