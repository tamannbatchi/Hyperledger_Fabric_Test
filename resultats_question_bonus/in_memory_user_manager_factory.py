from user_manager_factory import UserManagerFactory
from in_memory_user_manager import InMemoryUserManager
from user_manager import UserManager

# Implémentation de la Fabrique InMemoryUserManagerFactory qui implémente UserManagerFactory
# pour créer des instances de InMemoryUserManager

class InMemoryUserManagerFactory(UserManagerFactory):
# Méthode qui implémente la méthode abstraite de l'interface UserManagerFactory
    def create_user_manager(self) -> UserManager:
        return InMemoryUserManager()
