
from src.modules.auth.manager import auth_core
from src.schemas.user import UserRead, UserUpdate

excluded_routes = ["users:user", "users:patch_user", "users:delete_user"]


users_router = auth_core.get_users_router(UserRead, UserUpdate, requires_verification=True)
users_router.routes = [route for route in users_router.routes if route.name not in excluded_routes]
