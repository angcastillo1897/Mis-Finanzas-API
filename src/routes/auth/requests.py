from src.entities.user.schemas import UserCreate, UserLogin


class RegisterRequest(UserCreate):
    pass


class LoginRequest(UserLogin):
    pass
