from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import userEntity, usersEntity
from core.config import settings
from pymongo import MongoClient
from models.users_model import Users
from core.response import *
import pymongo
from bson.objectid import ObjectId
db = MongoClient(settings.MONGO_CONNECTION_STRING).ep_fastapi

user_router = APIRouter()


@user_router.get("/get", summary="Get one and all users")
async def get_users(id: str = None):
    if id != None:
        try:
            userData = userEntity(db.users.find_one({"_id": ObjectId(id)}))
        except:
            return badRequest("Invalid user id to get user data, please try again.")
    else:
        userData = usersEntity(db.users.find())
    return onSuccess("Users list", userData)


@user_router.post("/save", summary="Create and update user")
async def create_user(data: Users, id: str = None):
    if id != None:
        try:
            db.users.find_one_and_update(
                {"_id": ObjectId(id)}, {"$set": dict(data)})
            userData = userEntity(db.users.find_one({"_id": ObjectId(id)}))
            return onSuccess("User list", userData)
        except: 
            return badRequest("Invalid user id to update user data, please try again.")
    try:
        userExist = db.users.find_one({"$or": [{"email": data.email}, {"phone_no": data.phone_no}]})
        if userExist:
            return badRequest("User with this email or phone number already exist.")
        userID = db.users.insert_one(dict(data)).inserted_id
        userData = userEntity(db.users.find_one({"_id": ObjectId(userID)}))
        return onSuccess("User created successfull", userData)
    except pymongo.errors.DuplicateKeyError:
        return badRequest("User with this email or username already exist.")


@user_router.delete("/delete", summary="Get one and all users")
async def delete_users(id: str = None):
    try:
        userEntity(db.users.find_one_and_delete({"_id": ObjectId(id)}))
    except:
        return badRequest("Invalid user id to delete user data, please try again.")
    return onSuccess("User deleted successfull", 1)
