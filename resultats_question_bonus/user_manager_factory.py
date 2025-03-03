from abc import ABC, abstractmethod
from user_manager import UserManager

class UserManagerFactory(ABC):

# Méthode abstraite (qui doit être implémentée pour toute classe qui hérite de UserManagerFactory)
# qui retourne une instance de UserManager
    @abstractmethod
    def create_user_manager(self) -> UserManager:
        pass
