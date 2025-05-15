from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer  # Add this import
from sqlalchemy.orm import Session
from .. import models, schemas, database
from app.utils.auth import verify_password, create_access_token, decode_access_token, hash_password
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_pwd = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login/")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Make sure this is defined after the import

# Dependency to get the current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_access_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

@router.get("/users/me/", response_model=schemas.UserOut)
def get_user_profile(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

@router.put("/users/me/", response_model=schemas.UserOut)
def update_user_profile(
    updated_user: schemas.UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.id == current_user["user_id"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user details
    db_user.email = updated_user.email if updated_user.email else db_user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/me/password/", response_model=schemas.UserOut)
def change_password(
    old_password: str,
    new_password: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.id == current_user["user_id"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(old_password, db_user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    # Update the password
    db_user.password = hash_password(new_password)
    db.commit()
    db.refresh(db_user)
    return db_user


