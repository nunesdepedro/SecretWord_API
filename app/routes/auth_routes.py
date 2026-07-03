from datetime import datetime, timezone
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import UserRegister
from app.services.auth import create_refresh_token
from app.services.deps import get_current_user
from app.core.security import hash_password, verify_password, create_access_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
def register(user: UserRegister,
    db: Session = Depends(get_session)
):

    # check if user already exists
    user_exists = db.query(User).filter(User.email == user.email).first()

    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    new_user = User(
        email=user.email,
        username=user.username,
        password_hash=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created",
        "user_id": new_user.id
    }

@auth_router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):

    user = session.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    refresh_token, expire = create_refresh_token()

    db_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=expire
    )

    session.add(db_token)
    session.commit()

    return {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.post("/refresh")
def refresh(
    token: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    db_token = session.query(RefreshToken).filter(RefreshToken.token == token,
                                                  RefreshToken.revoked == False,
                                                  RefreshToken.user_id == current_user.id   
                                                  ).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    expires_at = db_token.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail="Expired refresh token"
        )

    access_token = create_access_token({"sub": str(db_token.user_id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@auth_router.post("/logout")
def logout(
    refresh_token: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_token = session.query(RefreshToken).filter(RefreshToken.token == refresh_token, RefreshToken.user_id == current_user.id, RefreshToken.revoked == False).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    db_token.revoked = True
    session.commit()

    return {
        "message": "Logged out successfully"
    }