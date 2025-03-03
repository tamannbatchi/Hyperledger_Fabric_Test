 #!/bin/bash

 # Variables de configuration
 MYSQL_CONTAINER="mysql"
 MYSQL_USER="user"
 MYSQL_PASSWORD="password"
 MYSQL_DATABASE="mydatabase"

 # Création de la table avec indexation
 SQL_COMMAND="
 CREATE TABLE IF NOT EXISTS users (
   user VARCHAR(100) NOT NULL,
   password VARCHAR(100) NOT NULL,
   PRIMARY KEY (user),
   INDEX (user)
 );
 "

 # Exécution de la commande SQL dans le conteneur mysql
 docker exec -i $MYSQL_CONTAINER mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE <<EOF
 $SQL_COMMAND
EOF

 # Vérification si la table a été créée avec succès
 if [ $? -eq 0 ]; then
     echo "Table 'users' créée avec succès dans la base de données '$MYSQL_DATABASE'."
 else
     echo "Erreur lors de la création de la table 'users'."
 fi
