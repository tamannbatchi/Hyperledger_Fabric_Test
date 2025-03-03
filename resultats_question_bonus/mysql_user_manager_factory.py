from user_manager_factory import UserManagerFactory
from mysql_user_manager import MySQLUserManager
from user_manager import UserManager

# Implémentation de la Fabrique MySQLUserManagerFactory qui implémente UserManagerFactory pour créer
# des instances de MySQLUserManager en passant les paramètres de connection à la base de donnée MySQL

class MySQLUserManagerFactory(UserManagerFactory):
# Méthode qui initialise la fabrique avec les paramètres de connection à la base de donnée MySQL
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

# Méthode qui implémente la méthode abstraite de l'interface UserManagerFactory
    def create_user_manager(self) -> UserManager:
        return MySQLUserManager(self.host, self.user, self.password, self.database)
