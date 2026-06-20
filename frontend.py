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
    fraud_row = {
        'Time': 406.0, 'V1': -2.312, 'V2': 1.951, 'V3': -1.609, 'V4': 3.997, 
        'V5': -0.522, 'V6': -1.426, 'V7': -2.537, 'V8': 1.391, 'V9': -2.770, 
        'V10': -2.772, 'V11': 3.202, 'V12': -2.899, 'V13': -0.595, 'V14': -4.289, 
        'V15': 0.389, 'V16': -1.140, 'V17': -2.830, 'V18': -0.016, 'V19': 0.416, 
        'V20': 0.126, 'V21': 0.517, 'V22': -0.035, 'V23': -0.465, 'V24': 0.320, 
        'V25': 0.044, 'V26': 0.177, 'V27': 0.261, 'V28': -0.143, 'Amount': 0.00
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
        
        
        API_URL = "https://stripe-fraud-api-xyz.onrender.com/predict" 
        
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