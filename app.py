import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

service_account_info = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])
GCP_SERVICE_ACCOUNT = {
  "type": "service_account",
  "project_id": "equipment-troubleshooter",
  "private_key_id": "c43d63fee57d817cc71bd7446235b6287539817f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCuEeTdIVTzY0bI\nlX82gT1eKNoIKr6S44NoQYcjop41CN1H1nk+hgVFLT8/oQykYyaRkJ0FyQq/ygXi\nOMb5dN76BbynTyWmJNs7v9Zj2goHwtz2fq69cDqsCfVNHc0i75cWhp0O5GQzjXNn\n7HC2MHcgz7lKpVK6uqdPBfg6eGII2thcDcJ7Cy8wMf22yT2Vgs5klYLXjXaNj4kR\nUqB5CDCeshtTfk0662GKCrsSO9U9GNfqTbJ6rFHRXyFH33ZpFONerugkdtN7nNBv\nARrI9Tt1jYqqo+SwvCetQWINh698co9rKenEqCUEUJtwaNPsIOViXr34++cOciqG\noYY7iLc5AgMBAAECggEAAyOAtfw0FaQ9FPW9dVsYzeNh72WDlJm3B1NY0iuhm2ke\nt1JuqCdUaJTKKAsu/jb+TX/hwEZ+89TFrM3IswZjKmIzLoJKy8oB7NFW1pZVBGKP\nEiqYMJjZqqY5Js6yTG6CRzZTwOkymtYykLrxUIGuIONJ+aaiknTLj+0r69765+Kw\nWWJMRS0PyZJS5JguJ5GKPRYPvDln4iSdn/8eT1GlZpNjZIOg7aHZPYCw+xbkhg8Z\n8tk3Ye4dZ1jYegkMaNFxE71VJ1z/4t4s8O4F7WDn616JJh2IliLadkwQGfwk6kr/\n/1Z0eTZSre8gyzeFtjAC9n+3JVIEc9KkocY/bVruMQKBgQDijqQCG5x24fVjqjp3\n8srqy8hIIAZcZIrKkzZIxrYm1XNKdEWy3gXlTLagOT4Kr0eKWIVyLWTU+TvM3wjf\nAEhE5TzwYjg0B5jMc8+6qY4zYviF7bd4fx35rgg2qVSk7Z9XtGhRADNp9w2gqBUX\n+tuvOq38X3FYvOfm3oYuLoO6UQKBgQDEsQwPLfoK5Wf7Txy0YJND6L9UxxOvMeRK\nPkuAswsIkto2r0kwJVwVtDHs1452EUwbSzatHIcdfy6kWMQCREPomw+xSq7JOGjU\nG+mebTqTI1qfTUDnIkJCgjXOeLMO8LoBx5wmksOgpdeBkDsylhBGVlY3ZYgKqCMz\nYbnwz42MaQKBgQCCyGTU8qt31SiayAHIjFenAswzFomVfFTCbAjCKjOsZzuOl2BE\nyPYOUCJ8i47NDDH4IvGl3559cwKaWYX9dWRCoTJ0cb6QCnKiU5hu4MI917wvU/K9\nlGPxZg1HwKgkLSf2sSYm3D7RxNQREfZbSWzX0r/tGAuOdj5If9xlfGR+gQKBgQC5\nT5juAEIw29vwoKOJqed1NqZ0yC7ag6Xy8OgPtB/0Du96UAEjVD+Cz0euPZQh1sAe\ngulbhaIi/z1BZ8Qb4pccYmMRhSxRtkzFchrTwVNLZyatKYq5eMR2htkM0xjYPaLx\npE+Q4/tdsoHstqefTFS+//6wqH7Yk3q+oRcfM1zH6QKBgQCDGK3YCmUGRTNKbGW3\n5kzqEbvTDRiFQI5SbvoxJ+wAWJhX87Wm6EbkohuPo+/mcq7gNDk3slxQ0WBteU3s\nyhoa7gXIrcLKL3hBXTQ96dexw+7ktcEv1FkOx0ZOjtNIcXbLjri33j2uv7QHqIXm\n2kVqUJcnYrSrTXtyPSFUuNJNkQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "medical-equipment-troubleshoot@equipment-troubleshooter.iam.gserviceaccount.com",
  "client_id": "110652730940100800727",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/medical-equipment-troubleshoot%40equipment-troubleshooter.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}



scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]


creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(creds)

sheet = client.open("MEDICAL_EQUIPMENT_ERRORS").sheet1

data = pd.DataFrame(sheet.get_all_records())



st.title("🔧 Medical Equipment Troubleshooter")

menu = st.sidebar.selectbox("Choose Action", ["Troubleshoot", "Add New Product"])

if menu == "Troubleshoot":
    # Dropdown for Product
    product = st.selectbox("Select Product", sorted(data["Product"].unique()))

    # Filter errors for selected product
    error_options = data[data["Product"] == product]["Error Description"].unique()
    error = st.selectbox("Select Error Description", sorted(error_options))

    # Find Solution
    solution = data[(data["Product"] == product) & (data["Error Description"] == error)]["Solution"].values
    if solution:
        st.success(f"✅ Solution: {solution[0]}")
    else:
        st.warning("⚠️ No solution found for this combination.")

elif menu == "Add New Product":
    st.subheader("➕ Add New Product & Error")

    # Input fields
    new_product = st.text_input("Enter Product Name")
    new_error = st.text_input("Enter Error Description")
    new_solution = st.text_area("Enter Solution")

    if st.button("Add to Database"):
        if new_product and new_error and new_solution:
            # Append to Google Sheet
            sheet.append_row([new_product, new_error, new_solution])
            st.success("✔️ New entry added successfully!")
        else:
            st.error("❌ Please fill all the fields.")
