"""员工接口路由：列表与创建，均需要登录。"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.features.employees import models, schemas

router = APIRouter(prefix="/api/employees", tags=["employees"])

@router.get("/departments", response_model=list[str])
def list_departments(current_user=Depends(get_current_user)):
    """返回可选的部门列表，供前端下拉框使用。"""
    return ["研发部", "产品部", "测试部", "人事部", "财务部"]

@router.get("/", response_model=list[schemas.EmployeeOut])
def list_employees(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """返回全部员工。未登录或 token 无效时返回 401。"""
    return db.query(models.Employee).all()


@router.post("/", response_model=schemas.EmployeeOut, status_code=201)
def create_employee(
    payload: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """创建员工。未登录或 token 无效时返回 401。"""
    employee = models.Employee(**payload.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee