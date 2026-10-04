from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    full_name: str
    email: str
    department: str
    is_active: bool = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    department: str | None = None
    is_active: bool | None = None


class EmployeeOut(EmployeeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)