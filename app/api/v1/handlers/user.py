from fastapi import APIRouter, BackgroundTasks, Body, Depends
from schemas.user_schema import userEntity, usersEntity
from models.users_model import Users
from schemas.permission_schema import permissionEntity, permissionsEntity
from core.security import get_password, verify_password, get_current_user
from core.config import settings
from pymongo import MongoClient
from core.response import *
import pymongo
import requests
import json
import re
import math
import random
from bson.objectid import ObjectId
from core.security import create_access_token
db = MongoClient(settings.MONGO_CONNECTION_STRING).ep_fastapi
headers = {
    'content-type': 'application/x-www-form-urlencoded'
}


def getReferralCode():
    code = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    referCode = ""
    for i in range(6):
        referCode += code[math.floor(random.random() * 36)]
    return referCode


user_router = APIRouter()


def set_user_permission(user, user_type):
    permission = permissionsEntity(db.permissions.find())
    for i in permission:
        if user_type == 1:
            if i["permission_name"] == "read" or i["permission_name"] == "update" or i["permission_name"] == "create":
                db.userpermissions.insert_one(
                    {"user_id": user["_id"], "permission_id": i["id"]})
        if user_type == 2:
            if i["permission_name"] == "read" or i["permission_name"] == "delete":
                db.userpermissions.insert_one(
                    {"user_id": user["_id"], "permission_id": i["id"]})
        if user_type == 3:
            if i["permission_name"] == "read" or i["permission_name"] == "update":
                db.userpermissions.insert_one(
                    {"user_id": user["_id"], "permission_id": i["id"]})
        if user_type == 4:
            if i["permission_name"] == "read" or i["permission_name"] == "update" or i["permission_name"] == "create" or i["permission_name"] == "delete":
                db.userpermissions.insert_one(
                    {"user_id": user["_id"], "permission_id": i["id"]})
        if user_type == 5:
            if i["permission_name"] == "read":
                db.userpermissions.insert_one(
                    {"user_id": user["_id"], "permission_id": i["id"]})


@user_router.get("/get", summary="Get one and all users", response_model=list)
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
async def create_user(background_tasks: BackgroundTasks, data: dict = Body(...)):
    if len(data["phone_no"]) == 10 and data["phone_no"] != '' and re.match("^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$", data["email"]) and data["email"] != '' and data["password"] != '' and len(data["password"]) >= 6:
        try:
            obj = {
                "name": data["name"],
                "email": data["email"],
                "phone_no": data["phone_no"],
                "password": get_password(data["password"]),
                "country_code": data["country_code"],
                "status" : False,
                "user_type": data["user_type"],
                "refer_code": data["refer_code"],
                "my_refer_code": getReferralCode(),
                "fcm_token": data["fcm_token"],
            }
            userExist = db.users.find_one(
                {"$or": [{"email": data["email"]}, {"phone_no": data["phone_no"]}]})
            if userExist:
                return badRequest("User with this email or phone number already exist.")
            url = settings.FACTOR_URL + data["phone_no"] + "/AUTOGEN"
            otpSend = requests.get(url, headers)
            response = json.loads(otpSend.text)
            if response["Status"] == "Success":
                userID = db.users.insert_one(obj).inserted_id
                userData = db.users.find_one({"_id": ObjectId(userID)})
                background_tasks.add_task(
                    set_user_permission, userData, data["user_type"])
                db.users.find_one_and_update({"_id": ObjectId(userID)}, {
                                             "$set": {"otpVerifyKey": response["Details"]}})
                return onSuccess("Otp send successfull", response)
            else:
                return badRequest("Something went wrong, unable to send otp for given mobile number, please try again!")
        except pymongo.errors.DuplicateKeyError:
            return badRequest("User with this email or username already exist.")
    else:
        return badRequest("Invalid data to register user, please try again!")


@user_router.post("/verifyotp", summary="User verify otp")
async def users_verify_otp(data: dict = Body(...)):
    if data["key"] != '' and data["phone_no"] != '' and len(data["phone_no"]) == 10 and data["otp"] != '' and len(data["otp"]) == 6:
        try:
            userExist = db.users.find_one(
                {"$or": [{"otpVerifyKey": data["key"]}, {"phone_no": data["phone_no"]}]})
            if userExist:
                url = settings.FACTOR_URL + "VERIFY/" + \
                    data["key"] + "/" + data["otp"]
                otpSend = requests.get(url, headers)
                response = json.loads(otpSend.text)
                if response["Status"] == "Success":
                    print("response[Status]", response["Status"])
                    db.users.find_one_and_update({"_id": ObjectId(userExist["_id"])}, {
                                                 "$set": {"mobileverified": True}})
                    return onSuccess("User mobile number verified successfully!", 1)
                else:
                    return badRequest("Invalid OTP, please try again")
            else:
                return badRequest("Invalid data to verify user mobile number, please try again")
        except:
            return badRequest("Invalid data to verify user mobile number, please try again")
    else:
        return badRequest("Invalid otp or mobile number to verify organizer mobile number, please try again")


@user_router.post("/login", summary="User Login")
async def login_user(data: dict = Body(...)):
    if data["phone_no"] != '' and len(data["phone_no"]) == 10 and data["password"] != '' and len(data["password"]) >= 6:
        try:
            userExist = db.users.find_one({"$or": [{"phone_no": data["phone_no"]}, {"status": True}, {"mobileverified": True}]})
            if userExist != '' and userExist["status"] == True:
                decPassword = verify_password(password=data["password"], hashed_pass=userExist["password"])
                if decPassword == True:
                    return onSuccess('User login successfully!', {"token" : create_access_token(userExist["_id"])})
                else:
                    return badRequest('Invalid password, please try again')
            else:
                return badRequest("Invalid mobile or password please try again")
        except:
            return badRequest("Invalid mobile or password please try again")
    else:
        return badRequest("Invalid mobile or password please try again")


@user_router.post("/currentuser", summary="Get current user by token")
async def test_token(user: Users = Depends(get_current_user)):
    return user


@user_router.delete("/delete", summary="Get one and all users")
async def delete_users(id: str = None):
    try:
        userEntity(db.users.find_one_and_delete({"_id": ObjectId(id)}))
    except:
        return badRequest("Invalid user id to delete user data, please try again.")
    return onSuccess("User deleted successfull", 1)
