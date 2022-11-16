import os
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from .models import Players
from .schema import TokenData
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from sql_app.db import get_db


SECRET_KEY = os.environ.get("KEY_DATABASE_URL")
ALGORITHM = os.environ.get("TOKEN_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 900000


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#аутентификация по логину и паролю
def verify_password(plain_password, hashed_password):
    """ Функция проверки пароля """
    return pwd_context.verify(plain_password, hashed_password)


def get_user_phone(db, phone: str):
    """ Функция поиска пользователя по номеру телефона """
    user_profile = db.query(Players).filter(Players.phone == phone).first()
    if user_profile:
        return user_profile
    else:
        return False

#аутентификация по токену
def get_user_id(db, user_id: str):
    """ Функция поиска пользователя по id """
    user_profile = db.query(Players).get(user_id)
    if user_profile:
        return user_profile
    else:
        return False


def authenticate_user(db, phone: int, password: str):
    """ Аутентификация пользователя по номеру телефона и паролю """
    user = get_user_phone(db, phone)
    if not user:
        return "Пользователя с таким логином не существует"
    if not verify_password(password, user.password):
        return "Пароль введен неверно"
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = get_user_id(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


# async def get_current_active_user(current_user: dict = Depends(get_current_user)):
#     # if current_user.disabled:
#     #     raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


#валидация токена
def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
