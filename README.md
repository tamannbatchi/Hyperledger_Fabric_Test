- Cloner ce dépôt: git clone https://github.com/tamannbatchi/Hyperledger_Fabric_Test.git
-  
 Ce dépôt est constitué de quatre répertoires principaux:
- Le répertoire "my-fabric-app": qui contient les résultats de la question3 de l'exercice
- Le répertoire "resultats_question2": qui contient les résultats de la question2 de l'exercice
- Le répertoire "resultat_question4": qui contient les résultats de la question4 de l'exercice
- Le répertoire "resultat_question_bonus": qui contient les résultats de la question_bonus de l'exercice

- Les fichiers de configuration (certificats, clés) et le bloc de genèse se trouvent (respectivement) dans les répertoires "crypto-config" et "channel-artifacts",
- qui sont deux sous-répertoires du répertoire "resultats_question2".

- Pour lancer les services "orderers" et "peers": Se placer dans le répertoire "resultats_question2" et taper la commande "docker-compose up -d".
- Pour lancer le service "mysql": Se placer dans le répertoire "resultats_question4" et taper la commande "docker compose -f docker-compose-sql.yml up -d mysql".
- Pour entrer dans le conteneur "mysql": taper la commande "docker exec -it mysql /bin/bash".
- Pour se connecter à MySQL: taper la commande "mysql -u user -p"
- Choisir la base de données "mydatabase": taper la commande "USE mydatabase"
- Pour afficher toutes les informations sur la table créée dans le répertoire "resultats__question4": taper la commande "SELECT * FROM users".

- Pour exécuter les fichiers ".sh" présents: Les rendre exécutables avec la commande "chmod +x nom_du_fichier", puis les exécuter avec la commande "./nom_du_fichier".

- Pour exécuter la fonction main de la question bonus (répertoire resultats_question_bonus): taper la commande "python3 main.py"
