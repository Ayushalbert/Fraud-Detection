import streamlit as st
import requests

st.set_page_config(page_title="Stripe Radar Clone", page_icon="🛡️", layout="centered")

st.title("🛡️ Stripe Radar Clone - Fraud Detection UI")
st.write("This UI is live-connected to your FastAPI ML backend. You can instantly check the risk score of any transaction.")

# Hardcoded templates taaki cloud par CSV file ki zaroorat na pade
@st.cache_data
def load_sample_templates():
    normal_row = {
        'Time': 0.0, 'V1': -1.359, 'V2': -0.072, 'V3': 2.536, 'V4': 1.378, 
        'V5': -0.338, 'V6': 0.462, 'V7': 0.239, 'V8': 0.098, 'V9': 0.363, 
        'V10': 0.090, 'V11': -0.551, 'V12': -0.617, 'V13': -0.991, 'V14': -0.311, 
        'V15': 1.468, 'V16': -0.470, 'V17': 0.207, 'V18': 0.025, 'V19': 0.403, 
        'V20': 0.251, 'V21': -0.018, 'V22': 0.277, 'V23': -0.110, 'V24': 0.066, 
        'V25': 0.128, 'V26': -0.189, 'V27': 0.133, 'V28': -0.021, 'Amount': 149.62
    }
    # An extreme outlier row that Isolation Forest will 100% catch as Anomaly
   # An extreme outlier row that Isolation Forest will 100% catch
    # An extreme outlier row that Isolation Forest will 100% catch
    fraud_row = {
        'Time': 100.0, 'V1': -10.5, 'V2': 8.2, 'V3': -15.4, 'V4': 8.5, 
        'V5': -9.1, 'V6': -3.2, 'V7': -12.5, 'V8': 7.1, 'V9': -6.3, 
        'V10': -11.2, 'V11': 6.5, 'V12': -10.1, 'V13': -1.2, 'V14': -12.3, 
        'V15': -0.5, 'V16': -8.1, 'V17': -13.5, 'V18': -4.5, 'V19': 2.1, 
        'V20': 1.5, 'V21': 2.2, 'V22': 0.1, 'V23': -0.5, 'V24': -0.2, 
        'V25': 0.5, 'V26': 0.2, 'V27': 1.1, 'V28': 0.5, 'Amount': 0.00
    }
    return normal_row, fraud_row

normal_tmpl, fraud_tmpl = load_sample_templates()

st.subheader("Step 1: Select a Transaction Template")
preset = st.radio(
    "What type of transaction would you like to simulate?",
    ("Normal Transaction Template", "Suspicious/Fraud Template")
)

base_data = normal_tmpl if preset == "Normal Transaction Template" else fraud_tmpl

st.subheader("Step 2: Modify Transaction Parameters")
amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=float(base_data['Amount']), step=10.0)
time_val = st.number_input("Time (Seconds from first tx)", min_value=0.0, value=float(base_data['Time']))

payload = {f"V{i}": float(base_data[f"V{i}"]) for i in range(1, 29)}
payload['Amount'] = amount
payload['Time'] = time_val

st.write("---")

if st.button("Analyze Transaction Risk 🔍", type="primary"):
    with st.spinner("ML Engine scanning the transaction..."):
        
        
        API_URL = "https://stripe-fraud-api.onrender.com/predict" 
        
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                status = result.get("transaction_status")
                action = result.get("action")
                
                if "FRAUD" in status:
                    st.error(f"### {status}")
                    st.warning(f"⚠️ **Stripe Radar Action:** {action}")
                else:
                    st.success(f"### {status}")
                    st.info(f"✅ **Stripe Radar Action:** {action}")
            else:
                st.error(f"API Error: Status Code {response.status_code}")
        except Exception as e:
            st.error(f"❌ Failed to connect to the backend API! Error: {e}")