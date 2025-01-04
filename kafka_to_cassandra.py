from kafka import KafkaConsumer
from cassandra.cluster import Cluster
import json

# Configuration Cassandra
cluster = Cluster(['localhost'])
session = cluster.connect()
session.set_keyspace('iot_keyspace')

# Configuration Kafka
consumer = KafkaConsumer(
    'iotdata',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='iot_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consommation des messages Kafka et insertion dans Cassandra
for message in consumer:
    data = message.value
    session.execute(
        """
        INSERT INTO sensor_data (sensor_id, timestamp, temperature, humidity)
        VALUES (%s, toTimestamp(now()), %s, %s)
        """,
        (data['sensor_id'], data['temperature'], data['humidity'])
    )
    print(f"Message inséré : {data}")
