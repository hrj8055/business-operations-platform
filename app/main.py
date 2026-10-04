from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Business Operations Platform")


@app.get("/")
def read_root():
    return {"message": "Business Operations Platform is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/employees/", response_model=schemas.EmployeeOut)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)


@app.get("/employees/", response_model=list[schemas.EmployeeOut])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_employees(db, skip=skip, limit=limit)


@app.get("/employees/{employee_id}", response_model=schemas.EmployeeOut)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@app.patch("/employees/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = crud.update_employee(db, employee_id, employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.delete_employee(db, employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}