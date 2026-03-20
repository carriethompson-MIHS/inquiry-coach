import streamlit as st
import requests
import json

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Senior Inquiry Coach", layout="centered")

st.title("🎓 Senior Inquiry Feedback Coach")

# --- 2. THE SIDEBAR KEY (Bypasses the 429 Error) ---
st.sidebar.header("Settings")
# We use a text input so you can paste the personal key directly
api_key = st.sidebar.text_input("Paste Personal API Key here:", type="password")
st.sidebar.info("Get a key at aistudio.google.com")

# --- 3. THE INPUTS ---
draft = st.text_area("Paste student work here:", height=300)

# --- 4. THE BRAIN ---
if st.button("Analyze My Work"):
    if not api_key:
        st.error("Please paste your API Key in the sidebar first!")
    elif not draft:
        st.warning("Please paste some text to analyze.")
    else:
        # March 2026: Gemini 1.5 Flash is the most stable free model
        model_id = "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1/models/{model_id}:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        prompt = f"Act as a teacher. Check this work for: 15 sources, no 'I/me/my' language, and MLA style. Work: {draft}"
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        with st.spinner("Analyzing..."):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
                result = response.json()
                
                if response.status_code == 200:
                    feedback = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("Success!")
                    st.markdown(feedback)
                else:
                    st.error(f"Google says: {result['error']['message']}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
