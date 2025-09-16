from dataclasses import dataclass
from typing import List, Optional

@dataclass
class User:
    id: int
    name: str
    email: str

    def __str__(self):
        return f"User: {self.name} <{self.email}>"

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

class UserService:
    def __init__(self):
        self._users: List[User] = []
        self._next_id = 1

    def add(self, name: str, email: str) -> User:
        if any(user.email == email for user in self._users):
            raise ValueError(f"Email {email} is already in use.")
        user = User(id=self._next_id, name=name, email=email)
        self._users.append(user)
        self._next_id += 1
        return user

    def get(self, user_id: int) -> Optional[User]:
        for user in self._users:
            if user.id == user_id:
                return user
        return None
    
    def getUserById(self, user_id: int) -> Optional[User]:
        return next((user for user in self._users if user.id == user_id), None)
    
    def searchByName(self, name: str) -> List[User]:
            name_lower = name.lower()
            return [user for user in self._users if user.name.lower() == name_lower]
    
    def list(self) -> List[User]:
        return list(self._users)

    def delete(self, user_id: int) -> bool:
        for i, user in enumerate(self._users):
            if user.id == user_id:
                del self._users[i]
                return True
        return False


if __name__ == "__main__":
    service = UserService()
    user1 = service.add("Alice", "alice@example.com")
    print(service.getUserById(user1.id))
    print(service.get(user1.id))
    service.searchByName("alice")
    service.searchByName("ALICE")