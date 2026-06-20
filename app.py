from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Initialize the FastAPI application
app = FastAPI(title="Stripe Radar Clone - Fraud Detection API")

# 1. Load the trained model and scaler into memory
print("Loading model and scaler...")
model = joblib.load("models/fraud_isolation_forest.joblib")
scaler = joblib.load("models/data_scaler.joblib")
print("Model loaded successfully!")

# 2. Pydantic Schema: Defines the expected incoming data format for the API
class Transaction(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float

# 3. Prediction Endpoint (/predict)
@app.post("/predict")
def predict_fraud(tx: Transaction):
    # Convert the transaction data into a dictionary
    data = tx.model_dump()
    
    # Arrange the columns in the exact order the model expects (V1-V28, scaled_amount, scaled_time)
    features = {f"V{i}": data[f"V{i}"] for i in range(1, 29)}
    
    # Scale the Time and Amount features (matching the training preprocessing step)
    features['scaled_amount'] = scaler.transform([[data['Amount']]])[0][0]
    features['scaled_time'] = scaler.transform([[data['Time']]])[0][0]
    
    # Convert to a DataFrame because the sklearn model expects this format
    X_input = pd.DataFrame([features])
    
    # Generate prediction (Isolation Forest: 1 = Normal, -1 = Anomaly/Fraud)
    prediction = model.predict(X_input)[0]
    
    # Return the appropriate response based on the prediction
    if prediction == -1:
        return {
            "transaction_status": "🔴 FRAUD DETECTED",
            "risk_score": -1,
            "action": "Block Transaction"
        }
    else:
        return {
            "transaction_status": "🟢 CLEAN",
            "risk_score": 1,
            "action": "Allow Transaction"
        }

# A simple root endpoint to verify that the API is running
@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running! Go to /docs to test."}