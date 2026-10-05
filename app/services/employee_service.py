from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app import crud, schemas


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    try:
        return crud.create_employee(db, employee)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="An employee with this email already exists")


def get_employee_or_404(db: Session, employee_id: int):
    db_employee = crud.get_employee(db, employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return crud.get_employees(db, skip=skip, limit=limit)


def update_employee(db: Session, employee_id: int, employee: schemas.EmployeeUpdate):
    db_employee = crud.update_employee(db, employee_id, employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = crud.delete_employee(db, employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee
