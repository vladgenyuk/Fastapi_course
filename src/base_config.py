from fastapi_users import FastAPIUsers
from auth.models import User
from auth.manager import get_user_manager
from auth.base_config import auth_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
