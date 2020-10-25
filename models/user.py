from dataclasses import dataclass


class AnonymousUser:
    pass


@dataclass
class User:
    id: int
    name: str
    username: str
    is_admin: bool

    def __post_init__(self):
        self.id = int(self.id)
        self.is_admin = True if self.is_admin == '1' else False
