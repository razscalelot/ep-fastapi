from datetime import datetime, timedelta
from fastapi import Depends
from passlib.context import CryptContext
from typing import Union, Any
from core.config import settings
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from schemas.user_schema import userEntity
from models.users_model import Users
from pydantic import ValidationError
from core.response import *
from bson.objectid import ObjectId
from pymongo import MongoClient
db = MongoClient(settings.MONGO_CONNECTION_STRING).ep_fastapi
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_VI_STR}/users/token",
    scheme_name="JWT"
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> str:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow(
        ) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    checkPermission = db.userpermissions.find({"$or": [{"user_id": ObjectId(subject)}]})

    permissionList = []
    for i in checkPermission:
        id = db.permissions.find_one({"$or": [{"_id": ObjectId(i["permission_id"])}]})
        permissionList.append(str(id["_id"]))    

    to_encode = {"exp": expires_delta, "sub": str(subject), "ext": permissionList}
    
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(reuseable_oauth)) -> Users:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            return badRequest("Token expired")
    except (jwt.JWTError, ValidationError):
        return badRequest("Could not validate credentials")

    print("payload", payload["ext"])
    access = db.permissions.find({"_id": [item for item in payload["ext"]]})
    
    # access = []
    # for i in payload["ext"]:
    #     per = db.permissions.find_one({"$or": [{"_id": ObjectId(i)}]})
    #     access.append(per)
    # print("access", access)
    user = userEntity(db.users.find_one({"_id": ObjectId(payload["sub"])}))
   
    if not user:
        return badRequest("Could not find user", 0)

    return onSuccess("User find successfull", user)
