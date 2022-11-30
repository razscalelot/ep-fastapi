from fastapi import FastAPI
from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_VI_STR}/openapi.json"
)


@app.on_event("startup")
async def app_init():
    """ initialize crucial application services """

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)

    await init_beanie(
        database=db_client.ap_fastapi,
        document_models=[

        ]
    )


# 0 - Super Admin
# 1 - Admin
# 2 - Sub Admin
# 3 - Excutive
# 4 - Organizer
# 5 - User