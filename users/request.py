from dataclasses import dataclass
from pydantic import EmailStr

@dataclass(frozen=True)
class SignUpRequest:
    name: str
    email: EmailStr
    password: str
    password_confirm: str

    def __post_init__(self):
        if self.password != self.password_confirm:
            raise ValueError('Password does not match')

    def to_user(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "password": make_password(self.password),
        }