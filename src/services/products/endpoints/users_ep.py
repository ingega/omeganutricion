# src/services/endpoints/materials_ep.py
from fastapi import Depends, Form, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import SecretStr

from src.services.products.schemas import UserCreate, UserUpdate, UserOut, User
from src.services.products.database import get_db
from src.services.products.crud import UserCrud
from src.services.products.auth import get_current_user, get_user, verify_password, password_hashed
from src.services.products.endpoints.utils import validate_password

router = APIRouter()

# constants
ROLE_EXCEPTION = HTTPException(status_code=403, detail="'user' role not allowed to update password")

# create a user
@router.post("/users", response_model=UserOut)
def create_user(username: Annotated[str, Form()],
                email: Annotated[str, Form()],
                password: Annotated[str, Form(json_schema_extra={'format':'password'})],
                confirm_password: Annotated[str, Form(json_schema_extra={'format':'password'})],
                full_name: Annotated[str, Form()],
                auth_level: Annotated[int, Form()] = 1,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)
                ):
    """
Creates a new user account. Requires Admin Authority.

This endpoint allows an authenticated user with sufficient authority (Auth Level 8+)
to register a new user in the system.

**Auth level for this endpoint**: 8

**Password Requirements:**
- Must contain at least 1 uppercase letter.
- Must contain at least 1 lowercase letter.
- Must contain at least 1 digit.
- Must contain at least 1 special character (e.g., . @ # _ - + *).

:param username: **The unique username for the new account.**
:param email:
    **The email address of the new user, used for communication
    and potentially password resets.**
:param password:
    **The primary password for the account. This will be hashed and never stored in plain text.**
:param confirm_password:
    **Re-enter the new password to confirm accuracy and avoid mistyping during registration.**
:param full_name:
    **The user's full, displayable name, which can be used in profile pages or internal logs.**
:param auth_level:
    **The initial authorization level of the user (1 is standard user, 8 is admin).**
:return: **The created User object.**
"""
    if current_user.auth_level < 8:
        raise ROLE_EXCEPTION
    # step 1, validate password format
    verify_format, message = validate_password(password)
    if not verify_format:
        raise HTTPException(status_code=400, detail=message)
    # step 2: verify password match
    if confirm_password != password:
        raise HTTPException(status_code=400, detail="password missmatch")
    user_crud = UserCrud(db=db)
    user = UserCreate(username=username, email=email, password=password,
                      full_name=full_name, auth_level=auth_level)
    return user_crud.create_user(user)

# get user info
@router.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int,
              current_user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    """
    This function returns the user information
    :param user_id: The id of the user
    :param db: The database session
    :return: Dictionary of the user information

    **Auth level for this endpoint**: 6
    """
    if current_user.auth_level < 6:
        raise ROLE_EXCEPTION
    user_crud = UserCrud(db=db)
    user = user_crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# update password
@router.put("/users/update-password/{username}", response_model=UserOut)
def update_user_password(username: str,
                         actual_password: SecretStr,  # protect password hijacking
                         new_password: SecretStr,  # necessary to compare and avoid typing errors
                         confirm_password: SecretStr,  # confirms new password to be saved
                         current_user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)
                         ):
    """
    This endpoint updates the password of the user.
    The user must provide either, old and new password.

    :param username: The username of the user

    :return: a Dictionary with the user information

    **Auth level for this endpoint**: 7
    """
    # the first validation: role. If user role is not admin, raise a 403
    user_auth_level = current_user.auth_level
    if user_auth_level < 1:
        raise ROLE_EXCEPTION
    # 1. get the user information, using get_user(username)
    user_data = get_user(username=username, db=db)
    # if user doesn't exist, get_user raise an Exception and returns a 404
    # 2. check the actual password
    plain_password = actual_password.get_secret_value()
    hashed_password = password_hashed(plain_password)
    verify = verify_password(plain_password, user_data.password)
    if not verify:
        raise HTTPException(status_code=400, detail="Incorrect password")
    # 3. verify the match of the new password
    if new_password.get_secret_value() != confirm_password.get_secret_value():
        raise HTTPException(status_code=400, detail="password missmatch")
    # 4. validate the password format
    verify_format, message = validate_password(new_password.get_secret_value())
    if not verify_format:
        raise HTTPException(status_code=400, detail=message)
    # 5. finally update information
    user_crud = UserCrud(db=db)
    # need a UserUpdate class
    user_update = UserUpdate(password=hashed_password)
    return user_crud.update_user(user_id=user_data.id, user=user_update)

@router.patch("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int,
                username: Annotated[str | None, Form()] = None,
                email: Annotated[str | None, Form()] = None,
                full_name: Annotated[str | None, Form()] = None,
                auth_level: Annotated[int | None, Form()] = None,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)
                ):
    """
    This endpoint update the user general data, but password.
    **Auth level for this endpoint**: 7
    """
    if current_user.auth_level < 7:
        raise ROLE_EXCEPTION
    user_data = {}
    if username:
        user_data['name'] = username
    if email:
        user_data['email'] = email
    if full_name:
        user_data['full_name'] = full_name
    if auth_level:
        user_data['auth_level'] = auth_level
    user_crud = UserCrud(db=db)
    user_schema = UserUpdate(**user_data)
    return user_crud.update_user(user_id=user_id, user=user_schema)


@router.delete("/users/{user_id}", response_model=UserOut)
def delete_user(user_id: int,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """
    This endpoint deletes the user from the database.
    **Auth level for this endpoint**: 8
    """
    # checking the auth level
    if current_user.auth_level < 8:
        raise ROLE_EXCEPTION
    user_crud = UserCrud(db=db)
    user = user_crud.delete_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or already deleted")
    return user
