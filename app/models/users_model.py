from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from core.config import settings
from bson.objectid import ObjectId

db = MongoClient(settings.MONGO_CONNECTION_STRING).ep_fastapi

class Users(BaseModel):
    name: str
    email: str
    phone_no: str
    password: str
    address: Optional[str] = None
    profile_pic: Optional[str] = None
    country_code: Optional[str] = None
    dob: Optional[str] = None
    about: Optional[str] = None
    refer_code: Optional[str] = None
    my_refer_code: Optional[str] = None
    fcm_token: Optional[str] = None
    user_type: Optional[int] = None
    status: Optional[bool] = False
    createdBy: Optional[str] = None
    updatedBy: Optional[str] = None
    
    @staticmethod
    async def get_user_by_id(id: str) -> Optional[str]:
        print("id", id)
        user = db.users.find_one({"_id": ObjectId(id)})
        return user
