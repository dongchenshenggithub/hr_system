from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth import models, schemas, security
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")

    user = models.User(
        username=payload.username,
        password_hash=security.hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user or not security.verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    token = security.create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@router.delete("/users/{username}", status_code=204)
def delete_user(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """删除指定用户。只允许用户删除自己，防止越权删除他人账号。"""
    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只能删除自己的账号",
        )

    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    db.delete(user)
    db.commit()
    return None
