from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    login: str
    password_hash: str
    name: str
    surname: str
    patronymic: str | None
    phone: str | None
    user_role: int
    balance: float
    # Служебное поле: название роли из таблицы UserRole (в User не хранится)
    role_name: str | None = None

    @property
    def full_name(self) -> str:
        parts = [self.surname, self.name, self.patronymic]
        return " ".join(p for p in parts if p)
