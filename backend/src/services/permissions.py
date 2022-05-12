from fastapi import HTTPException, Depends

from loggers import get_logger
from .auth import get_current_user
from models import User


logger = get_logger(__name__)


class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")


# "role"  с правом на создание нового "user"
allow_create_new_user = RoleChecker(["admin"])

# "role"  с правом на получение записи из таблицы
allow_get_items = RoleChecker(["admin", "manager"])

# "role"  с правом на создание новой записи в таблицу
allow_create_items = RoleChecker(["admin", "manager"])

# "role"  с правом на изменение записи в таблице
allow_update_items = RoleChecker(["admin"])

# "role"  с правом на удаление записи из таблицы
allow_delete_items = RoleChecker(["admin"])
