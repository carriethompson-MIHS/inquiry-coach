import streamlit as st
import requests
import json

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Senior Inquiry Coach", layout="centered")

st.title("🎓 Senior Inquiry Feedback Coach")

# --- 2. THE SIDEBAR (API KEY) ---
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Paste Personal API Key here:", type="password")
st.sidebar.info("Get your key at aistudio.google.com")

# --- 3. THE INPUTS (Restored Toggle) ---
mode = st.radio("What are you working on?", ["Building the Outline", "Writing the Full Paper"])
draft = st.text_area("Paste student work here:", height=300)

# --- 4. THE BRAIN ---
if st.button("Analyze My Work"):
    if not api_key:
        st.error("Please paste your API Key in the sidebar first!")
    elif not draft:
        st.warning("Please paste some text to analyze.")
    else:
        # 🚀 2026 UPDATE: Switching to the active 2.5-flash model
        model_id = "gemini-2.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1/models/{model_id}:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        
        # Adjusting the prompt based on the toggle
        if mode == "Building the Outline":
            prompt_intro = "Check this OUTLINE for logical flow and source count (needs 15)."
        else:
            prompt_intro = "Check this PAPER for MLA style and first-person language (no 'I/me/my')."

        prompt = f"Act as a teacher. {prompt_intro} Work: {draft}"
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        with st.spinner("Connecting to 2026 Google Servers..."):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
                result = response.json()
                
                if response.status_code == 200:
                    feedback = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("Analysis Complete!")
                    st.markdown(feedback)
                elif response.status_code == 404:
                    st.error("Google says the model ID is wrong. Trying legacy alias...")
                else:
                    st.error(f"Google says: {result['error']['message']}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
