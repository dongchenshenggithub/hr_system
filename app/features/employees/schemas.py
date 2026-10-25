from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str | None = None


class EmployeeOut(BaseModel):
    id: int
    name: str
    email: str
    department: str | None

    model_config = {"from_attributes": True}
