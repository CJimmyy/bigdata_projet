from pyspark.sql import SparkSession
from cassandra.cluster import Cluster

# Tester la connexion à Cassandra
try:
    cluster = Cluster(['cassandra']) 
    session = cluster.connect()
    print("Connexion à Cassandra réussie.")
    cluster.shutdown()
except Exception as e:
    print(f"Erreur de connexion à Cassandra : {e}")



# Créer une session Spark
spark = SparkSession.builder \
    .appName("SparkCassandraIntegration") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.cassandra.connection.port", "9042") \
    .getOrCreate()

# Lire les données depuis Cassandra
df = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="sensor_data", keyspace="iot_keyspace") \
    .load()

# Afficher les données
df.show()

# Appliquer une transformation (exemple : moyenne de la température)
df.groupBy("sensor_id").avg("temperature").show()

# Arrêter Spark
spark.stop()
