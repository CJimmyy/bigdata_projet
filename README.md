# **Big Data Project: IoT Data Pipeline**

Ce projet met en place une pipeline de traitement de données pour simuler et analyser des données de l'Internet des Objets (IoT). La pipeline comprend la génération de données par un simulateur, leur ingestion via Apache Kafka, leur traitement avec Apache Spark, et leur stockage dans une base de données Cassandra.

---

## **Table des matières**

1. [Description](#description)
2. [Technologies utilisées](#technologies-utilisées)
3. [Configuration et installation](#configuration-et-installation)
4. [Utilisation](#utilisation)
5. [Fonctionnalités](#fonctionnalités)
6. [Problèmes rencontrés](#problèmes-rencontrés)
7. [Contributions](#contributions)



## **Description**

Ce projet vise à construire une infrastructure distribuée pour :
- Simuler des données IoT.
- Envoyer les données via Kafka.
- Stocker les données dans une base Cassandra.
- Traiter et analyser les données avec Spark.

L'objectif est de démontrer l'intégration de ces technologies pour gérer des flux de données et répondre à des cas d'utilisation.



## **Technologies utilisées**

- **Kafka** : Système de messagerie distribuée pour transporter les données IoT.
- **Cassandra** : Base de données NoSQL pour le stockage des données IoT.
- **Spark** : Framework de traitement de données distribué pour analyser les données.
- **Docker & Docker-Compose** : Conteneurisation et orchestration des services.

---

## **Pré-requis**

1. [Install Docker](https://docs.docker.com/desktop/)


## **Configuration et installation**

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/CJimmyy/bigdata_projet.git
   ```

2. **Configurer l'environnement Python :**

    Créer un environnement virtuel :
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Installer les dépendances :**

    ```bash
    pip install kafka-python
    pip install cassandra-driver
    ```

4. **Démarrer les services Docker :**

    Utiliser Docker Compose pour lancer les conteneurs :
    ```bash
    docker-compose up -d
    ```

5. **Vérifier les services :**

    Accédez à l'interface de Kafka, Spark, et Cassandra pour vérifier leur disponibilité. 
    ```bash
    docker ps
    ```  

## **Utilisation**

1. **Créer le topic :**

   ```bash
    docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic iotdata --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    ```
  

2. **Consommer le topic :**

  ```bash
    docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic iotdata --from-beginning
  ```

3. **Produire le message :**

  Vous pouvez créer votre propre message avec :
  ```bash
  docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic iotdata
  ```
  Dans notre cas on utilisera un script : iot_simulator.py

4. **Lister les topics :**

  ```bash
    docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
  ```

5. **Créer une table cassandra :**

  ```bash
  docker exec -it cassandra cqlsh

  CREATE KEYSPACE iot_keyspace
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

  USE iot_keyspace;

  CREATE TABLE sensor_data (
      sensor_id INT,
      timestamp TIMESTAMP,
      temperature FLOAT,
      humidity FLOAT,
      PRIMARY KEY (sensor_id, timestamp)
  );
  ```

6. **Lancer le simulateur IoT :**

   ```bash
   python3 scripts/iot_simulator.py
   ```

7. **Lancer l'enregistrement dans cassandra:**

    ```bash
    python3 scripts/kafka_to_cassandra.py
    ```

8. **Installez un connector spark cassandra:**

  Vous devez d'abord installez le connecteur : [spark-cassandra-connector_2.12-3.5.1.jar](https://mvnrepository.com/artifact/com.datastax.spark/spark-cassandra-connector_2.12/3.5.1) 

  ```bash
  docker exec -it spark bash
  ls /opt/bitnami/spark/jars/

  docker cp jars/spark-cassandra-connector_2.12-3.5.1.jar spark:/opt/bitnami/spark/jars/
  ```
  Dans notre cas, la connexion spark et cassandra fonctionnent mais, lors du chargement '.load()' il y a une erreur. J'ai éssayé d'ajouter d'autres jars mais ça ne fonctionne toujours pas.

  ```bash
  docker cp jars/spark-cassandra-connector-driver_2.12-3.5.1.jar spark:/opt/bitnami/spark/jars/

  docker cp jars/java-driver-core-4.14.0.jar spark:/opt/bitnami/spark/jars/

  docker cp jars/guava-30.1-jre.jar spark:/opt/bitnami/spark/jars/
  ```

9. **Exécuter la pipeline Spark-Cassandra :**
    ```bash
    spark-submit --master local[*] \
    --jars jars/spark-cassandra-connector_2.12-3.5.1.jar\
    scripts/kafka_to_cassandra.py
    ```
  Vous pouvez voir le Spark Master UI  sur <http://localhost:8080>

## **Fonctionnalités**

- **Simulation de données IoT :**  
  - Génération de flux de données simulées.  

- **Pipeline de traitement :**  
  - Envoi des données via Kafka.  
  - Stockage dans Cassandra.  
  - Analyse avec Spark (en temps stream ou batch proccessing).

## **Problèmes rencontrés**

- **Connexion :**  
  - S'assurer que les différents services sont dans le même réseau.
  ```bash
  docker network ls
  docker network inspect <bigdata_projet>
  ```

- **Intégration Spark-Cassandra :**  
  - Configuration complexe des connecteurs pour assurer leur compatibilité.  

- **Gestion des dépendances JAR :**  
  - Compatibilité entre les versions des bibliothèques et résolution des conflits.
    


## **Contributions**

- **Jimmy CAI**  
