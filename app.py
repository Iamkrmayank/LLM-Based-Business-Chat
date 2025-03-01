import streamlit as st
import pandas as pd
from neon import create_table, insert_data, fetch_all_data
from llm import validate_data

st.title("📄 LLM Data Verification System")
st.sidebar.title("Chat with Data 🤖")

# Upload CSV File
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    if st.button("Validate & Store"):
        create_table()
        for index, row in df.iterrows():
            try:
                validation = validate_data(row)
                status = "Valid" if "Valid" in validation else "Invalid"
                reviews = int(row["reviews"]) if "reviews" in df.columns and pd.notna(row["reviews"]) else 0
                rating = float(row["rating"]) if "rating" in df.columns and pd.notna(row["rating"]) else 0.0
                latitude = float(row["latitude"]) if "latitude" in df.columns and pd.notna(row["latitude"]) else 0.0
                longitude = float(row["longitude"]) if "longitude" in df.columns and pd.notna(row["longitude"]) else 0.0
                
                insert_data(
                    row["name"], row["address"], row["website"], row["phone_number"],
                    reviews, rating, latitude, longitude, status
                )
                st.write(f"✅ {row['name']} - {status}")
            except Exception as e:
                st.error(f"Error processing {row['name']}: {e}")

st.subheader("📌 Verified Data")
data = fetch_all_data()
if data:
    st.table(pd.DataFrame(data, columns=["ID", "Name", "Address", "Website", "Phone Number", "Reviews", "Rating", "Latitude", "Longitude", "Status", "Verified At"]))
else:
    st.info("No Verified Data Available")

# Chatbot Section
# Chatbot Section
st.sidebar.subheader("💬 Chat with Verified Data")
user_input = st.sidebar.text_input("Ask me anything about the data")

if st.sidebar.button("Chat"):
    if user_input:
        # Fetch all verified data
        data = fetch_all_data()
        df = pd.DataFrame(data, columns=["ID", "Name", "Address", "Website", "Phone Number", "Reviews", "Rating", "Latitude", "Longitude", "Status", "Verified At"])

        if not df.empty:
            # Convert DataFrame to JSON for better context
            data_context = df.to_json(orient="records")

            # Now pass the entire data context and user query to GPT
            prompt = f"""You are a data assistant.
            Here is the verified business dataset:
            {data_context}

            Question: {user_input}
            Please answer the question based on the data provided only."""
            
            # Send prompt to GPT
            response = validate_data({"query": prompt})
            st.sidebar.write(response)
        else:
            st.sidebar.info("No verified data available.")
    else:
        st.sidebar.warning("Please enter your question.")





