from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app import crud, schemas, security
from app.logging_config import logger


def register_user(db: Session, user: schemas.UserCreate):
    try:
        new_user = crud.create_user(db, user)
        logger.info(f"New user registered: {new_user.username}")
        return new_user
    except IntegrityError:
        db.rollback()
        logger.warning(f"Registration failed, username already exists: {user.username}")
        raise HTTPException(status_code=400, detail="Username already registered")


def login_user(db: Session, username: str, password: str):
    user = crud.authenticate_user(db, username, password)
    if user is None:
        logger.warning(f"Failed login attempt for username: {username}")
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    logger.info(f"User logged in: {username}")
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
