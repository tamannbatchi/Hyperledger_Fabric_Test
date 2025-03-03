 #!/bin/bash

 # Variables de configuration
 MYSQL_CONTAINER="mysql"
 MYSQL_USER="user"
 MYSQL_PASSWORD="password"
 MYSQL_DATABASE="mydatabase"

 # insertion, lecture, mise à jour, et lecture de l'utilisateur
 SQL_COMMANDS="
 INSERT INTO users (user, password) VALUES ('Tamann', 'initialPassword');
 SELECT * FROM users WHERE user='Tamann';
 UPDATE users SET password='updatedPassword' WHERE user='Tamann';
 SELECT * FROM users WHERE user='Tamann';
 "

 # Exécution des commandes SQL dans le conteneur mysql
 docker exec -i $MYSQL_CONTAINER mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE <<EOF
 $SQL_COMMANDS
EOF

 # Vérification si les commandes ont été exécutées avec succès
 if [ $? -eq 0 ]; then
     echo "Opérations sur la table 'users' réalisées avec succès."
 else
     echo "Erreur lors des opérations sur la table 'users'."
 fi
