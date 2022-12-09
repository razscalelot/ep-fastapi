from fastapi import FastAPI
from core.config import settings
from api.v1.router import router
from pymongo import MongoClient
db = MongoClient(settings.MONGO_CONNECTION_STRING).ep_fastapi

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_VI_STR}/openapi.json"
)


@app.on_event("startup")
async def app_init():
    try:
        crud = ["create", "read", "update", "delete", "approve", "disapprove"]
        collection = db.list_collection_names()
        for i in collection:
            if i == "contenttypes" or i == "permissions" or i == "userpermissions":
                continue
            userExist = db.contenttypes.find_one({"collection_name": i})
            if userExist:
                continue
            contenttype = db.contenttypes.insert_one({"collection_name": i}).inserted_id
            for j in crud:
                crudExist = db.permissions.find_one({"permission_name": j})
                if crudExist:
                    continue
                db.permissions.insert_one({"contenttype_id": contenttype, "permission_name": j})
    except:
        return None

app.include_router(router, prefix=settings.API_VI_STR)