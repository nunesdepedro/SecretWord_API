from fastapi import Depends, HTTPException

from app.services.auth import decode_token
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.services.auth import decode_token
from app.models.user import User


from app.dependencies.auth import oauth2_scheme

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):

    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = int(payload["sub"])

    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user
