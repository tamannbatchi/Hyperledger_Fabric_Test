from mysql_user_manager_factory import MySQLUserManagerFactory
from in_memory_user_manager_factory import InMemoryUserManagerFactory

def main():
    # Utilisation de la fabrique MySQLUserManagerFactory
    # Création d'une instance de MySQLUserManagerFactory en utilisant les paramètres de connection à la base de donnée MySQL
    mysql_factory =  MySQLUserManagerFactory('localhost', 'root', 'rootpassword', 'mydatabase')

    # Utilisation de la fabrique pour créer une instance de MySQLUserManager
    mysql_user_manager = mysql_factory.create_user_manager()

    # Ajout, lecture, mise à jour et suppression d'un utilisateur
    mysql_user_manager.add_user('mysql_user', 'mysql_password')
    user = mysql_user_manager.get_user('mysql_user')
    print(f"MySQL User: {user}")

    mysql_user_manager.update_user('mysql_user', 'new_mysql_password')
    user = mysql_user_manager.get_user('mysql_user')
    print(f"Updated MySQL User: {user}")

    mysql_user_manager.delete_user('mysql_user')
    user = mysql_user_manager.get_user('mysql_user')
    print(f"Deleted MySQL User: {user}")

    # Utilisation de la fabrique InMemoryUserManagerFactory
    # Création d'une instance de InMemoryUserManagerFactory
    memory_factory = InMemoryUserManagerFactory()

    # Utilisation de la fabrique pour créer une instance de InMemoryUserManager
    memory_user_manager = memory_factory.create_user_manager()

    # Ajout, lecture, mise à jour et suppression d'un utilisateur
    memory_user_manager.add_user('memory_user', 'memory_password')
    user = memory_user_manager.get_user('memory_user')
    print(f"In-Memory User: {user}")

    memory_user_manager.update_user('memory_user', 'new_memory_password')
    user = memory_user_manager.get_user('memory_user')
    print(f"Updated In-Memory User: {user}")

    memory_user_manager.delete_user('memory_user')
    user = memory_user_manager.get_user('memory_user')
    print(f"Deleted In-Memory User: {user}")

if __name__ == "__main__":
    main()
