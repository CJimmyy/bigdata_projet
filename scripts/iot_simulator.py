import time
import json
from kafka import KafkaProducer
import random
from kafka.errors import KafkaError

# Initialisation du producteur Kafka pour envoyer des messages au topic 'iotdata'
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Génère des données de capteurs de manière continue
# Envoie les données au topic Kafka
def generate_sensor_data():
    while True:
        data = {
            "sensor_id": random.randint(1, 100),
            "temperature": round(random.uniform(15.0, 30.0), 2),
            "humidity": round(random.uniform(30.0, 70.0), 2),
            "timestamp": time.time()
        }

        try:
            future = producer.send('iotdata', value=data)
            metadata = future.get(timeout=10)  # Attente du résultat de l'envoi
            print(f"Message envoyé avec succès au topic {metadata.topic}, partition {metadata.partition}, offset {metadata.offset}")
        except KafkaError as e:
            print(f"Erreur lors de l'envoi : {e}")
        time.sleep(1)

if __name__ == "__main__":
    generate_sensor_data()
