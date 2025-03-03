import mysql.connector
from user_manager import UserManager

class MySQLUserManager(UserManager):

    def __init__(self, host, user, password, database):
        # Initialisation d'une connection à la base de données MySQL en utilisant les paramètres fournis
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )


    def add_user(self, user: str, password: str):
        # Création d'un curseur pour exécuter des commandes SQL
        cursor = self.connection.cursor()

        # Exécution d'une commande SQL pour insérer un nouvel utilisateur et son mot de passe dans la table 'users'
        cursor.execute("INSERT INTO users (user, password) VALUES (%s, %s)", (user, password))

        # Enrégistrement des modifications dans la base de données
        self.connection.commit()


    def get_user(self, user: str) -> dict:
        cursor = self.connection.cursor()

        # Exécution d'une commande SQL pour récupérer les informations de l'utilisateur spécifié
        cursor.execute("SELECT user, password FROM users WHERE user=%s", (user,))

        # Récupération du résultat de la requête
        result = cursor.fetchone()

        # Retourne les informations de l'utilisateur sous forme de dictionnaire, ou None si l'utilisateur n'existe pas
        return {"user": result[0], "password": result[1]} if result else None


    def update_user(self, user: str, new_password: str):
        cursor = self.connection.cursor()

        # Exécution d'une commande SQL pour mettre à jour le mot de passe de l'utilisateur spécifié
        cursor.execute("UPDATE users SET password=%s WHERE user=%s", (new_password, user))

        # Enrégistrement des modifications dans la base de données
        self.connection.commit()


    def delete_user(self, user: str):
        cursor = self.connection.cursor()

        # Exécution d'une commande SQL pour supprimer l'utilisateur spécifié de la table 'users'
        cursor.execute("DELETE FROM users WHERE user=%s", (user,))

        #  Enrégistrement des modifications dans la base de données
        self.connection.commit()


    def __del__(self):
        # Ferméture de la connection à la base de données lorsque l'instance de MySQLUserManager est détruite
        self.connection.close()
