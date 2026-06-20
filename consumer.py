from kafka import KafkaConsumer
import json
import requests

# Kafka consumer setup - listening to the 'live_transactions' topic
consumer = KafkaConsumer(
    'live_transactions',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Target URL for your FastAPI backend endpoint
API_URL = "http://localhost:8000/predict"

print("🎧 Listening for real-time transactions...")

# Process each new message as it arrives in the continuous stream
for message in consumer:
    transaction_data = message.value
    
    # Send a POST request to the prediction API with the transaction data
    try:
        response = requests.post(API_URL, json=transaction_data)
        result = response.json()
        
        status = result.get('transaction_status')
        amount = transaction_data.get('Amount')
        
        if "FRAUD" in status:
            print(f"🚨 [ALERT] Fraud Detected! Amount: ${amount} | Action: {result.get('action')}")
        else:
            print(f"✅ [OK] Clean Transaction. Amount: ${amount}")
            
    except Exception as e:
        print(f"❌ API Error: {e}")