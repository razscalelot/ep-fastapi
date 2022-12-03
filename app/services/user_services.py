from schemas.user_schema import UserAuth
from models.users_model import Users
from core.security import get_password, verify_password

class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        user_in = Users(
            phone_no=user.phone_no,
            email=user.email,
            password=get_password(user.password)
        )
        await user_in.save()
        return user_in