from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from models import UserCreate, User, Token

import services


router = APIRouter(
    prefix="/auth",
    tags=['auth'],
    # default_response_class=JSONResponse
)


@router.post(
    path="/sign-up/",
    response_model=Token
)
def sign_up(
    user_data: UserCreate,
    service: services.AuthService = Depends(),
    # зависимость "allowed" дает право создавать нового пользователя,
    # только пользователям "role" котрых указаны в "allow_create_new_user"
    allowed: services.allow_create_new_user = Depends()
):
    return service.register_new_user(user_data)


@router.post(
    path="/sign-in",
    response_model=Token,
)
def sign_in(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: services.AuthService = Depends(),
):
    token = auth_service.authenticate_user(
        auth_data.username,
        auth_data.password
    )
    # response = Response()
    # response.headers['Authorization'] = f'Bearer {token.access_token}'
    return token



@router.get(
    path="/user/",
    response_model=User
)
def get_user(
    # token: str
    # token (из http-headers) "клиента" передается в функцию get.current_user
    allowed: services.allow_create_new_user = Depends(),
    user: User = Depends(services.get_current_user)
):
    return user
