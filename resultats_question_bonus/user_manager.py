from abc import ABC, abstractmethod

class UserManager(ABC):

    # Méthode abstraite pour ajouter un utilisateur 
    @abstractmethod
    def add_user(self, user: str, password: str):
        pass

    # Méthode abstraite pour lire un utilisateur
    @abstractmethod
    def get_user(self, user: str) -> dict:
        pass

    # Méthode abstraite pour mettre à jour le mot de passe d'un utilisateur
    @abstractmethod
    def update_user(self, user: str, new_password: str):
        pass

    # Méthode abstraite pour supprimer un utilisateur
    @abstractmethod
    def delete_user(self, user: str):
        pass
