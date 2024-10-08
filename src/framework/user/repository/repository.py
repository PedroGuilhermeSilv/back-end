from src.core.user.domain.dto.user_dto import UserOutPut
from src.core.user.domain.entity import User
from src.core.user.domain.exceptions.user_exceptions import UserAlreadyExistError
from src.core.user.domain.repository.user_repository import UserRepository
from src.framework.user.models import User as UserModel


class DjangoORMUserRepository(UserRepository):
    def __init__(self, user_model: UserModel):
        self.user_model = user_model

    def save(self, user: User) -> UserOutPut:
        if self.user_model.objects.filter(email=user.email).exists():
            raise UserAlreadyExistError
        user_model = self.user_model.objects.create(
            email=user.email,
            password=user.password,
            id=user.id,
        )
        return UserOutPut(
            email=user_model.email,
            password=user_model.password,
            id=user_model.id,
        )

    def get_by_email(self, email: str) -> UserOutPut:
        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            return None
        return UserOutPut(email=user.email, password=user.password, id=user.id)
