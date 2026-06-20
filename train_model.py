import os
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def train_fraud_detector():
    # 1. Load the Data
    print("⏳ Loading dataset...")
    data_path = "data/creditcard.csv"
    
    if not os.path.exists(data_path):
        print(f"❌ Error: {data_path} not found! Please place the Kaggle dataset in the 'data' folder first.")
        return
        
    df = pd.read_csv(data_path)
    print(f"✅ Data loaded successfully! Total Rows: {df.shape[0]}, Total Columns: {df.shape[1]}")

    # 2. Understand the Data (Highly Imbalanced Dataset)
    # The dataset contains a 'Class' column: 0 = Normal, 1 = Fraud
    frauds = df[df['Class'] == 1]
    normal = df[df['Class'] == 0]
    contamination_rate = len(frauds) / len(normal)
    print(f"📊 Normal Transactions: {len(normal)} | Fraud Transactions: {len(frauds)}")
    print(f"📉 Contamination Rate (Fraud %): {contamination_rate:.4f}")

    # 3. Data Preprocessing
    # The 'Time' and 'Amount' columns have varying scales, so they must be normalized.
    # The other columns (V1-V28) are already PCA-transformed (normalized).
    print("⚙️ Preprocessing data using StandardScaler...")
    scaler = StandardScaler()
    df['scaled_amount'] = scaler.fit_transform(df['Amount'].values.reshape(-1, 1))
    df['scaled_time'] = scaler.fit_transform(df['Time'].values.reshape(-1, 1))

    # Drop the original 'Time', 'Amount', and target 'Class' columns to prepare the feature set
    X = df.drop(['Time', 'Amount', 'Class'], axis=1)
    
    # 4. Train the Isolation Forest Model
    # Isolation Forest is ideal for anomaly detection because it isolates fraud points (outliers) quickly.
    print("🤖 Starting model training (Isolation Forest)...")
    
    model = IsolationForest(
        n_estimators=100,          # Number of decision trees to build
        max_samples='auto',        # Number of samples drawn to train each tree
        contamination=0.0017,      # Expected percentage of frauds in the dataset (approx 0.17%)
        random_state=42,           # Seed for reproducible results
        n_jobs=-1                  # Utilize all available CPU cores for faster training
    )

    # Train the model purely on the features (X) in an unsupervised manner
    model.fit(X)
    print("✅ Model training completed!")

    # 5. Save the Model and Scaler
    # Saving is essential so the FastAPI backend can utilize them without needing to retrain.
    print("💾 Saving model and scaler...")
    os.makedirs("models", exist_ok=True)
    
    joblib.dump(model, "models/fraud_isolation_forest.joblib")
    joblib.dump(scaler, "models/data_scaler.joblib")
    
    print("🎉 Everything successfully saved in the 'models/' folder!")

if __name__ == "__main__":
    train_fraud_detector()