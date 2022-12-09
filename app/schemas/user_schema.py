from pydantic import BaseModel
from typing import Optional
class UserEntity(BaseModel):
    _id: str
    name: str
    email: str
    phone_no: str
    address: Optional[str]
    profile_pic: Optional[str]
    country_code: Optional[str]
    my_refer_code: Optional[str]
    dob: Optional[str]
    about: Optional[str]

def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "phone_no": item["phone_no"],
        "country_code": item["country_code"],
        "my_refer_code": item["my_refer_code"],
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]
