def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "phone_no": item["phone_no"],
        "address": item["address"],
        "profile_pic": item["profile_pic"],
        "country_code": item["country_code"],
        "my_refer_code": item["my_refer_code"]
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]
