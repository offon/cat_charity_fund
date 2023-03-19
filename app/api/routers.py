from fastapi import APIRouter

from app.api.endpoints import (charityproject_router, donation_router,
                               google_api_router, user_router)
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

user_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
user_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(charityproject_router, prefix='/charity_project', tags=['charity_projects'])
main_router.include_router(donation_router, prefix='/donation', tags=['donation'])
main_router.include_router(google_api_router, prefix='/google', tags=['Google'])