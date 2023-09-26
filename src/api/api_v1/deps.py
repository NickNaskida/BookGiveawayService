from src.modules.auth.manager import auth_core


# User dependencies
current_active_user = auth_core.current_user(active=True)
