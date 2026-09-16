from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select

from app.database import SessionLocal
from app.models import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.dependencies import get_current_user


router = APIRouter()


# =========================
# Public Endpoints
# =========================

@router.post("/users")
def create_user(user_data: UserCreate):
    db = SessionLocal()

    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }


@router.post("/login")
def login(user_data: UserLogin):
    db = SessionLocal()

    user = db.scalar(
        select(User).where(User.email == user_data.email)
    )

    if user is None:
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user_data.password, user.password):
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    db.close()

    token = create_access_token({
        "sub": str(user.id)
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# Authenticated Endpoints
# =========================

@router.get("/users/me")
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }


@router.put("/users/{id}")
def update_user(
    id: int,
    user_data: UserCreate,
    current_user: User = Depends(get_current_user)
):
    # Make sure the user can only update their own account
    if id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own account"
        )

    db = SessionLocal()

    user = db.get(User, id)

    if user is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.name = user_data.name
    user.email = user_data.email
    user.password = hash_password(user_data.password)

    db.commit()
    db.refresh(user)
    db.close()

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }


@router.delete("/users/{id}")
def delete_user(
    id: int,
    current_user: User = Depends(get_current_user)
):
    # Make sure the user can only delete their own account
    if id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own account"
        )

    db = SessionLocal()

    user = db.get(User, id)

    if user is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()
    db.close()

    return {
        "message": "User deleted successfully"
    }
