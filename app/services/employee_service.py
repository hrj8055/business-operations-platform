from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app import crud, schemas
from app.logging_config import logger


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    try:
        new_employee = crud.create_employee(db, employee)
        logger.info(f"Employee created: id={new_employee.id}, email={new_employee.email}")
        return new_employee
    except IntegrityError:
        db.rollback()
        logger.warning(f"Duplicate employee email attempted: {employee.email}")
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
    logger.info(f"Employee updated: id={employee_id}")
    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = crud.delete_employee(db, employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    logger.info(f"Employee deleted: id={employee_id}")
    return db_employee
