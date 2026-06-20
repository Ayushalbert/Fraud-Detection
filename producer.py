import pandas as pd
from kafka import KafkaProducer
import json
import time

# Kafka producer setup - Sends data in JSON format
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("🚀 Starting Live Transaction Stream...")

# Load the dataset
df = pd.read_csv('data/creditcard.csv')

# Stream each row as a new transaction
for index, row in df.iterrows():
    # Drop the 'Class' column (fraud label), as the API will predict this
    transaction_data = row.drop('Class').to_dict()
    
    # Send the transaction data to the 'live_transactions' Kafka topic
    producer.send('live_transactions', value=transaction_data)
    print(f"[{index}] Sent transaction for Amount: ${transaction_data['Amount']}")
    
    # Add a 1-second delay to simulate a real-time stream
    time.sleep(1)