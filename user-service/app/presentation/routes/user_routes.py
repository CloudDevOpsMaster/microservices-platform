from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated
from app.application.dtos.user_dto import (
    CreateUserRequest, UpdateUserRequest, UserResponse, UserListResponse
)
from app.application.use_cases.create_user_use_case import CreateUserUseCase
from app.presentation.dependencies import (
    get_create_user_use_case,
    get_current_user
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    use_case: Annotated[CreateUserUseCase, Depends(get_create_user_use_case)],
    current_user: Annotated[dict, Depends(get_current_user)]
) -> UserResponse:
    """
    Create a new user (Admin only).
    
    - **email**: Valid email address (unique)
    - **full_name**: User's full name (min 2 chars)
    - **role**: user, admin, or moderator
    - **phone**: Optional phone number
    - **department**: Optional department
    """
    # Check if current user is admin
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create users"
        )
    
    try:
        return await use_case.execute(request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User creation failed"
        )


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "user-service"}