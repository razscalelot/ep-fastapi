from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import userEntity, usersEntity
from core.config import settings
from pymongo import MongoClient
from models.users_model import Users
from core.response import *
import pymongo
from bson import ObjectId



user_router = APIRouter()

@user_router.get("/", summary="Get all users")
async def get_users():
    userData = usersEntity(MongoClient(settings.MONGO_CONNECTION_STRING).ep_fastapi.users.find())
    return onSuccess("Users list", userData)

@user_router.post("/create", summary="Create new user")
async def create_user(data: Users):
    try:
        userData = MongoClient(settings.MONGO_CONNECTION_STRING).ep_fastapi.users.insert_one(dict(data))
        return usersEntity(MongoClient(settings.MONGO_CONNECTION_STRING).ep_fastapi.users.find_one({"_id": ObjectId(userData.id)}))
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist."
        )
