import os
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Import logging configuration
from logging_config import (
    get_logger,
    log_api_call,
    log_business_event,
    log_execution_time,
)

# Initialize logger for this module
logger = get_logger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypass@db:5432/mydb")
logger.info(
    f"🔗 Database connection established",
    database_url=DATABASE_URL.split("@")[1] if "@" in DATABASE_URL else DATABASE_URL,
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)


class UserCreate(BaseModel):
    name: str
    email: str
    is_active: bool = True


class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

    class Config:
        orm_mode = True
        from_attributes = True


app = FastAPI()

# Tạo bảng nếu chưa có
logger.info("🗃️ Creating database tables if they don't exist")
Base.metadata.create_all(bind=engine)


@log_execution_time
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
@log_api_call
def root():
    return {"message": "Welcome to Senior Python FastAPI!", "status": "healthy"}


@app.post("/users/", response_model=User)
@log_api_call
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("👤 Creating new user", user_name=user.name, user_email=user.email)

    # Check if user already exists
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user:
        logger.warning("⚠️ User already exists", email=user.email)
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.success(
        "✅ User created successfully",
        user_id=db_user.id,
        user_name=db_user.name,
        user_email=db_user.email,
    )

    # Log business event
    log_business_event(
        "user_created",
        user_id=db_user.id,
        user_email=db_user.email,
        is_active=db_user.is_active,
    )

    return db_user


@app.get("/users/", response_model=List[User])
@log_api_call
def list_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    logger.info("📋 Listed all users", user_count=len(users))
    return users


@app.get("/users/{user_id}", response_model=User)
@log_api_call
def get_user(user_id: int, db: Session = Depends(get_db)):
    logger.info("🔍 Fetching user", user_id=user_id)
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        logger.warning("⚠️ User not found", user_id=user_id)
        raise HTTPException(status_code=404, detail="User not found")

    logger.success("✅ User found", user_id=user.id, user_name=user.name)
    return user


@app.put("/users/{user_id}", response_model=User)
@log_api_call
def update_user(user_id: int, updated: UserCreate, db: Session = Depends(get_db)):
    logger.info("✏️ Updating user", user_id=user_id)
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        logger.warning("⚠️ User not found for update", user_id=user_id)
        raise HTTPException(status_code=404, detail="User not found")

    old_email = user.email
    user.name = updated.name
    user.email = updated.email
    user.is_active = updated.is_active
    db.commit()
    db.refresh(user)

    logger.success(
        "✅ User updated successfully",
        user_id=user.id,
        old_email=old_email,
        new_email=user.email,
    )

    # Log business event
    log_business_event(
        "user_updated",
        user_id=user.id,
        old_email=old_email,
        new_email=user.email,
    )

    return user


@app.delete("/users/{user_id}")
@log_api_call
def delete_user(user_id: int, db: Session = Depends(get_db)):
    logger.info("🗑️ Deleting user", user_id=user_id)
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        logger.warning("⚠️ User not found for deletion", user_id=user_id)
        raise HTTPException(status_code=404, detail="User not found")

    user_email = user.email
    db.delete(user)
    db.commit()

    logger.success(
        "✅ User deleted successfully", user_id=user_id, user_email=user_email
    )

    # Log business event
    log_business_event("user_deleted", user_id=user_id, user_email=user_email)

    return {"ok": True}


@app.get("/users/active", response_model=List[User])
@log_api_call
def get_active_users(db: Session = Depends(get_db)):
    active_users = db.query(UserDB).filter(UserDB.is_active == True).all()
    logger.info("🟢 Listed active users", active_user_count=len(active_users))
    return active_users
