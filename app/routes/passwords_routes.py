from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.models.user import User
from app.schemas.password import PasswordCreate, PasswordUpdate
from app.models.password import Passwords
from app.services.encryption import decrypt_password, encrypt_password, MASTER_KEY
from app.services.deps import get_current_user

passwords_routes = APIRouter(prefix="/passwords", tags=["passwords"])


@passwords_routes.get("/")
async def root_list_passwords(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

            passwords = session.query(Passwords).filter(
                Passwords.user_id == current_user.id
            ).all()

            return {"message": "Here initiates the application",
                        "password": [
                {
                    "id": password.id,
                    "website": password.website,
                    "username": password.username,
                    "notes": password.notes
                }
                for password in passwords
            ]
        }


#cretae pass
@passwords_routes.post("/add_secretword")
def add_secretword(
    passwords_schema: PasswordCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    encrypted = encrypt_password(MASTER_KEY, passwords_schema.password)

    new_password = Passwords(
        website=passwords_schema.website,
        username=passwords_schema.username,
        password_encrypted=encrypted,
        notes=passwords_schema.notes,
        user_id=current_user.id
    )

    session.add(new_password)
    session.commit()
    session.refresh(new_password)

    return {"message": "Password saved"}

@passwords_routes.get("/{password_id}")
def get_password(
    password_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    password = (
        session.query(Passwords)
        .filter(
            Passwords.id == password_id,
            Passwords.user_id == current_user.id
        )
        .first()
    )

    if password is None:
        raise HTTPException(
            status_code=404,
            detail="Password not found"
        )

    return {
        "id": password.id,
        "website": password.website,
        "username": password.username,
        "password": decrypt_password(MASTER_KEY, password.password_encrypted),
        "notes": password.notes
    }

#update pass
@passwords_routes.put("/{password_id}")
def update_password(
    password_id: int,
    passwords_schema: PasswordUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    password = (
        session.query(Passwords)
        .filter(
            Passwords.id == password_id,
            Passwords.user_id == current_user.id
        )
        .first()
    )

    if password is None:
        raise HTTPException(
            status_code=404,
            detail="Password not found"
        )

    if passwords_schema.website is not None:
        password.website = passwords_schema.website

    if passwords_schema.username is not None:
        password.username = passwords_schema.username

    if passwords_schema.password is not None:
        password.password_encrypted = encrypt_password(MASTER_KEY,
            passwords_schema.password
        )

    if passwords_schema.notes is not None:
        password.notes = passwords_schema.notes

    session.commit()
    session.refresh(password)

    return {
        "message": "Password updated successfully"
    }


#delete pass
@passwords_routes.delete("/{password_id}")
def delete_password(
    password_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    password = (
        session.query(Passwords)
        .filter(
            Passwords.id == password_id,
            Passwords.user_id == current_user.id
        )
        .first()
    )

    if password is None:
        raise HTTPException(
            status_code=404,
            detail="Password not found"
        )

    session.delete(password)
    session.commit()

    return {
        "message": "Password deleted successfully"
    }