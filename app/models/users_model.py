from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Users(BaseModel):
    name: str
    email: str
    phone_no: str
    password: str
    address: Optional[str]
    profile_pic: Optional[str]
    country_code: Optional[str]
    refer_code: Optional[int]
    my_refer_code: Optional[int]
    fcm_token: Optional[str]
    user_type: Optional[int]
    status: Optional[bool]
    createdBy: Optional[str]
    updatedBy: Optional[str]
