from thelibrary.domain.value_objects import Email, PasswordHash, UserId, UserName


class User:
    def __init__(
        self, id: UserId, username: UserName, email: Email, password_hash: PasswordHash
    ):
        self._id: UserId = id
        self._username: UserName = username
        self._email: Email = email
        self._password_hash: PasswordHash = password_hash

    @property
    def id(self) -> UserId:
        return self._id

    @property
    def username(self) -> UserName:
        return self._username

    @property
    def email(self) -> Email:
        return self._email

    @property
    def password_hash(self) -> PasswordHash:
        return self._password_hash

    @classmethod
    def create(
        cls, 
        id: UserId, 
        username: UserName, 
        email: Email, 
        password_hash: PasswordHash
    ) -> User:
        return cls(
            id=id, 
            username=username, 
            email=email, 
            password_hash=password_hash
        )

    def change_email(self, new_email: Email) -> None:
        if self._email == new_email:
            return
        self._email = new_email

    def change_username(self, new_username: UserName) -> None:
        if self._username == new_username:
            return
        self._username = new_username

    def __str__(self) -> str:
        return f"User(id={self.id}, username={self.username})"
