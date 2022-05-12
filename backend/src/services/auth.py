from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
from jose import jwt, JWSError
from pydantic import ValidationError
from database import get_session
from sqlalchemy.orm import Session
from time import sleep

import tables
import models
from settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:
    return AuthService.verify_token(token)


class AuthService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session


    @classmethod
    def verify_password(cls, raw_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(raw_password, hashed_password)


    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)


    @classmethod
    def verify_token(cls, token: str) -> models.User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate creditionals",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algoritm]
            )
        except JWSError:
            raise exception from None

        user_data = payload.get("user")
        try:
            user = models.User.parse_obj(user_data)
        except ValidationError:
            raise exception from None
        return user


    @classmethod
    def create_token(cls, user: tables.User) -> models.Token:
        user_data = models.User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=settings.jwt_expiration),
            "sud": str(user_data.id),
            "user": user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algoritm
        )
        # print('start')
        # sleep(3)
        # print('stop')
        return models.Token(access_token=token)


    def register_new_user(self, user_data: models.UserCreate) -> models.Token:
        user = tables.User(
            email=user_data.email,
            username=user_data.username,
            role = user_data.role,
            password_hash=self.hash_password(user_data.password)
        )
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)


    def authenticate_user(self, username: str, password: str) -> models.Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
        user = (
            self.session.query(tables.User)
            .filter_by(username=username)
            .first()
        )
        if not user:
            raise exception
        if not self.verify_password(password, user.password_hash):
            raise exception
        return self.create_token(user)
