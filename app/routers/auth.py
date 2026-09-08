from fastapi import APIRouter, HTTPException, status

from app.config import settings
from app.schemas import LoginRequest, TokenResponse
from app.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    if (
        credentials.username != settings.admin_username
        or credentials.password != settings.admin_password
    ):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Usuario o contraseña incorrectos"
        )
    token = create_access_token(subject=credentials.username)
    return TokenResponse(access_token=token)
