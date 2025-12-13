from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Annotated

from app.application.dtos.auth_dto import (
    LoginRequest, LoginResponse, RefreshTokenRequest,
    RegisterRequest, UserResponse
)
from app.application.use_cases.login_use_case import LoginUseCase
from app.application.use_cases.refresh_token_use_case import RefreshTokenUseCase
from app.application.use_cases.register_use_case import RegisterUseCase
from app.presentation.dependencies import get_login_use_case, get_refresh_use_case, get_register_use_case

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    use_case: Annotated[RegisterUseCase, Depends(get_register_use_case)]
) -> UserResponse:
    """
    Register a new user.
    
    - **email**: Valid email address
    - **password**: Min 8 chars, must contain uppercase, lowercase, and digit
    - **full_name**: User's full name (min 2 chars)
    """
    try:
        return await use_case.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    http_request: Request,
    use_case: Annotated[LoginUseCase, Depends(get_login_use_case)]
) -> LoginResponse:
    """
    Authenticate user and return JWT tokens.
    
    - **email**: User's email
    - **password**: User's password
    
    Returns access_token (30min) and refresh_token (7 days)
    """
    try:
        return await use_case.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed")


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    use_case: Annotated[RefreshTokenUseCase, Depends(get_refresh_use_case)]
) -> LoginResponse:
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    
    Returns new access_token
    """
    try:
        return await use_case.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token refresh failed")


@router.post("/logout")
async def logout(
    # TODO: Implement token blacklisting
) -> dict:
    """Logout user (invalidate tokens)."""
    return {"message": "Logged out successfully"}


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "auth-service"}