from user_manager import UserManager

class InMemoryUserManager(UserManager):

    def __init__(self):
        # Initialisation du dictionnaire
        self.users = {}


    def add_user(self, user: str, password: str):
        # Ajout d'un nouvel utilisateur avec son mot de passe dans le dictionnaire
        if user in self.users:
            raise ValueError(f"{user} already exists")
        self.users[user] = password


    def get_user(self, user: str):
        # Affichage d'un utilisateur et son mot de passe
        if user not in self.users:
            raise ValueError(f"{user} is not in users.")
        return (user, self.users[user])


    def update_user(self, user: str, updatedpassword: str):
        # Mise à jour du mot de passe
        if user not in self.users:
            raise ValueError(f"{user} is not in users.")
        self.users[user] = updatedpassword


    def delete_user(self, user: str):
        # Suppression de l'utilisateur
        if user not in self.users:
            raise ValueError(f"{user} is not in users.")
        del self.users[user]
