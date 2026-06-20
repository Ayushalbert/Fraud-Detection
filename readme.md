# 🛡️ Real-Time Fraud Detection API (Stripe Radar Clone)

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![Kafka](https://img.shields.io/badge/Apache_Kafka-Event_Streaming-black.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Machine_Learning-orange.svg)

## 📌 Project Overview
This project is a real-time, event-driven machine learning pipeline designed to detect fraudulent credit card transactions. Inspired by systems like Stripe Radar, it streams transaction data through Apache Kafka and scores them for risk in real-time using an Isolation Forest anomaly detection model exposed via FastAPI.

## 🏗️ Architecture & Data Flow
1. **Producer (`producer.py`)**: Simulates real-time user traffic by streaming transactions from a Kaggle dataset into a Kafka topic.
2. **Event Stream (Apache Kafka)**: Acts as the message broker, handling high-throughput transaction streams.
3. **Consumer (`consumer.py`)**: Subscribes to the Kafka topic, ingests events, and forwards them to the ML backend.
4. **Scoring Engine (FastAPI + ML)**: Receives the data, applies standard scaling, and uses a pre-trained **Isolation Forest** model to classify the transaction as `CLEAN` or `FRAUD` in milliseconds.

## ⚙️ Tech Stack
* **Backend Framework:** FastAPI (Python)
* **Message Broker / Streaming:** Apache Kafka, Zookeeper
* **Machine Learning:** Scikit-Learn (Isolation Forest), Pandas, Joblib
* **Environment:** macOS (Homebrew managed)

## 📂 Project Structure
```text
fraud-detection-api/
│
├── data/
│   └── creditcard.csv                 # Kaggle Dataset
├── models/
│   ├── fraud_isolation_forest.joblib  # Trained ML Model
│   └── data_scaler.joblib             # Standard Scaler
│
├── train_model.py                     # ML Training Script
├── app.py                             # FastAPI Application
├── producer.py                        # Kafka Producer (Fake Stream)
├── consumer.py                        # Kafka Consumer & API Client
└── requirements.txt                   # Project Dependencies