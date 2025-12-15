"""User routes - Presentation Layer"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated

from app.application.dtos.user_dto import (
    CreateUserRequest, UpdateUserRequest, UserResponse, UserListResponse
)
from app.application.use_cases.create_user_use_case import CreateUserUseCase
from app.application.use_cases.get_users_use_case import GetUsersUseCase, GetUserByIdUseCase
from app.application.use_cases.update_user_use_case import UpdateUserUseCase
from app.application.use_cases.delete_user_use_case import DeleteUserUseCase
from app.presentation.dependencies import (
    get_create_user_use_case,
    get_get_users_use_case,
    get_get_user_by_id_use_case,
    get_update_user_use_case,
    get_delete_user_use_case,
    get_current_user
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "user-service"}


@router.get("", response_model=UserListResponse)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    use_case: Annotated[GetUsersUseCase, Depends(get_get_users_use_case)] = None,
    current_user: Annotated[dict, Depends(get_current_user)] = None
) -> UserListResponse:
    """
    Get paginated list of users.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (1-1000)
    
    Requires authentication.
    """
    try:
        return await use_case.execute(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    use_case: Annotated[GetUserByIdUseCase, Depends(get_get_user_by_id_use_case)] = None,
    current_user: Annotated[dict, Depends(get_current_user)] = None
) -> UserResponse:
    """
    Get user by ID.
    
    - **user_id**: User identifier
    
    Requires authentication.
    """
    try:
        return await use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user: {str(e)}"
        )


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    use_case: Annotated[CreateUserUseCase, Depends(get_create_user_use_case)] = None,
    current_user: Annotated[dict, Depends(get_current_user)] = None
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


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    request: UpdateUserRequest,
    use_case: Annotated[UpdateUserUseCase, Depends(get_update_user_use_case)] = None,
    current_user: Annotated[dict, Depends(get_current_user)] = None
) -> UserResponse:
    """
    Update user information.
    
    - **user_id**: User identifier
    - **full_name**: Updated full name (optional)
    - **phone**: Updated phone (optional)
    - **department**: Updated department (optional)
    - **role**: Updated role (optional, admin only)
    - **is_active**: Updated active status (optional, admin only)
    
    Users can update their own info. Admins can update any user.
    Only admins can change role and is_active fields.
    """
    # Check permissions
    is_own_profile = current_user.get("id") == user_id
    is_admin = current_user.get("role") == "admin"
    
    if not is_own_profile and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )
    
    # Non-admins cannot change role or is_active
    if not is_admin:
        if request.role is not None or request.is_active is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can change role or active status"
            )
    
    try:
        return await use_case.execute(user_id, request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    use_case: Annotated[DeleteUserUseCase, Depends(get_delete_user_use_case)] = None,
    current_user: Annotated[dict, Depends(get_current_user)] = None
) -> None:
    """
    Delete user (Admin only).
    
    - **user_id**: User identifier
    
    Only admins can delete users.
    """
    # Check if current user is admin
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete users"
        )
    
    # Prevent self-deletion
    if current_user.get("id") == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    try:
        await use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )