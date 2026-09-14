from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.database import SessionLocal
from app.models import User
from app.schemas.user import UserCreate,UserLogin
from app.utils.security import hash_password, verify_password, create_access_token
router = APIRouter()

# =========================
# Create User
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
#---------login-------------#
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
# get Users
# =========================

@router.get("/users")
def get_users():

    db = SessionLocal()

    users = db.scalars(select(User)).all()

    db.close()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in users
    ]


# =========================
# get User by Id
# =========================

@router.get("/users/{id}")
def get_users(id:int):

    db = SessionLocal()

    user = db.get(User,id)
    user = db.get(User, id)

    if user is None :
        db.close()
        raise HTTPException(
        status_code=404,
        detail="User not found"
    )
    db.close()

    return{
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

# =========================
# update User by Id
# =========================


@router.put("/users/{id}")
def update_user(id:int,user_data:UserCreate):
    dp=SessionLocal()

    user=dp.get(User,id)

    if user is None :
            dp.close()
            raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    user.name=user_data.name
    user.email=user_data.email

    dp.commit()
    dp.refresh(user)
    dp.close()

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email 
    }

# =========================
# delete User by Id
# =========================

@router.delete("/users/{id}")
def delete_user(id: int):

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