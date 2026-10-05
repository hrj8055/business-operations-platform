from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas, security
from app.database import engine, get_db
from app.services import employee_service, user_service

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Business Operations Platform")


@app.get("/")
def read_root():
    return {"message": "Business Operations Platform is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, user)


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return user_service.login_user(db, form_data.username, form_data.password)


@app.post("/employees/", response_model=schemas.EmployeeOut)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    return employee_service.create_employee(db, employee)


@app.get("/employees/", response_model=list[schemas.EmployeeOut])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return employee_service.get_employees(db, skip=skip, limit=limit)


@app.get("/employees/{employee_id}", response_model=schemas.EmployeeOut)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    return employee_service.get_employee_or_404(db, employee_id)


@app.patch("/employees/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(
    employee_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    return employee_service.update_employee(db, employee_id, employee)


@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    employee_service.delete_employee(db, employee_id)
    
    return {"message": "Employee deleted"}
