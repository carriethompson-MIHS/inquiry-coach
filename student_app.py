import streamlit as st
import requests
import json

st.set_page_config(page_title="Senior Inquiry Coach - Student Version", layout="centered")
st.title("🎓 Senior Inquiry Feedback Coach")

# --- 1. HIDDEN KEY (From Secrets) ---
# This looks for the key in your Streamlit dashboard secrets
api_key = st.secrets["MY_API_KEY"]

# --- 2. THE INPUTS ---
mode = st.radio("Phase:", ["Building the Outline", "Writing the Full Paper"])
draft = st.text_area("Paste your text here:", height=300)

# --- 3. THE BRAIN ---
if st.button("Analyze My Work"):
    if not draft:
        st.warning("Please paste some text.")
    else:
        model_id = "gemini-2.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1/models/{model_id}:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        prompt = f"Act as a teacher. Check this work for: 15 sources, no 'I/me/my' language, and MLA style. Work: {draft}"
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        with st.spinner("Analyzing..."):
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                st.success("Analysis Complete!")
                st.markdown(response.json()['candidates'][0]['content']['parts'][0]['text'])
            else:
                st.error("The coach is busy. Please wait 60 seconds and try again.")
