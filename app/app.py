from fastapi import FastAPI
from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.users_model import Users
from models.permissions_model import Permissions, UserPermissions
from api.v1.router import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_VI_STR}/openapi.json"
)


@app.on_event("startup")
async def app_init():
    """ initialize crucial application services """

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)

    await init_beanie(
        database=db_client.ep_fastapi,
        document_models=[
            Users,
            Permissions,
            UserPermissions,
        ]
    )


app.include_router(router, prefix=settings.API_VI_STR)