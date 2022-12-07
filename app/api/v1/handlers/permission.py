from fastapi import APIRouter
from schemas.permission_schema import permissionEntity, permissionsEntity
from core.response import *
from core.config import settings
from pymongo import MongoClient
from models.permissions_model import Permissions
import pymongo
from bson.objectid import ObjectId
db = MongoClient(settings.MONGO_CONNECTION_STRING).ep_fastapi


permission_router = APIRouter()

@permission_router.get("/get", summary="Get one and all users")
async def get_permission(id: str = None):
    if id != None:
        try:
            permissionData = permissionEntity(db.permissions.find_one({"_id": ObjectId(id)}))
        except:
            return badRequest("Invalid permission id to get permission data, please try again.")
    else:
        permissionData = permissionsEntity(db.permissions.find())
    return onSuccess("Users list", permissionData)

@permission_router.post("/create", summary="Create new permission")
async def create_permission(data: Permissions, id: str = None):
    if id != None:
        try:
            db.permissions.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(data)})
            permissionData = permissionEntity(db.permissions.find_one({"_id": ObjectId(id)}))
            return onSuccess("Permission list", permissionData)
        except: 
            return badRequest("Invalid permission id to update permission data, please try again.")
    try:
        permissionExist = db.permissions.find_one({"$or": [{"permission_name": data.permission_name}]})
        if permissionExist:
            return badRequest("Permission with this name already exist.")
        permissionID = db.permissions.insert_one(dict(data)).inserted_id
        permissionData = permissionEntity(db.permissions.find_one({"_id": ObjectId(permissionID)}))
        return onSuccess("User created successfull", permissionData)
    except pymongo.errors.DuplicateKeyError:
        return badRequest("Permission with this name already exist.")

@permission_router.delete("/delete", summary="Delete one and all permission")
async def delete_permission(id: str = None):
    try:
        permissionEntity(db.permissions.find_one_and_delete({"_id": ObjectId(id)}))
    except:
        return badRequest("Invalid permission id to delete permission data, please try again.")
    return onSuccess("Permission deleted successfull", 1)