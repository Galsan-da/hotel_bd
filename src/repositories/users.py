from src.repositories.base import BaseRepository
from src.models.users import UsersOrm

class UsersRepository(BaseRepository):
    model = UsersOrm