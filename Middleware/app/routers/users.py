from fastapi import APIRouter
from pydantic import BaseModel
from typing import Union
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


users = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

class User(BaseModel):
    user_id: str
    password: str
    platform: str

class Permission(BaseModel):
    auth_token: str
    permission: str
    platform: str

@users.post("/signup", status_code=201)
async def signup(user: User):
    """
    Endpoint for user signup.

    Args:
        user (User): User object containing user information.

    Returns:
        dict: Empty dictionary.
    """
    logging.info(f'signup: {user}')
    return {}

@users.post("/login")
async def login(user: User):
    """
    Endpoint for user login.

    Args:
        user (User): User object containing user information.

    Returns:
        dict: Dictionary containing authentication token.
    """
    logging.info(f'login: {user}')
    return {
        "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    }

@users.post("/permission")
async def permission(user: Permission):
    """
    Endpoint for user permission.

    Args:
        user (User): User object containing user information.

    Returns:
        dict: Empty dictionary.
    """
    logging.info(f'permission: {user}')
    return {}