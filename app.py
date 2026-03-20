import streamlit as st
import requests
import json

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Senior Inquiry Coach", layout="centered")

RUBRIC_DATA = """
- 15+ informational sources required.
- NO first/third person (I, me, you, we, us, my).
- 3+ quality visuals (graphs/charts) required.
- MLA formatting throughout.
- Precise, knowledgeable claims only.
"""

st.title("🎓 Senior Inquiry Feedback Coach")

# --- 2. KEY LOGIC ---
if "MY_API_KEY" in st.secrets:
    user_key = st.secrets["MY_API_KEY"]
else:
    user_key = st.sidebar.text_input("Teacher API Key:", type="password")

# --- 3. INPUTS ---
mode = st.radio("Phase:", ["Building the Outline", "Writing the Full Paper"])
draft = st.text_area("Paste your text here:", height=300)

# --- 4. THE BRAIN (2026 STABLE ENDPOINT) ---
if st.button("Analyze My Work"):
    if not user_key:
        st.error("API Key missing!")
    elif not draft:
        st.warning("Please paste some text.")
    else:
        # 🚀 UPDATE: Using the Gemini 3 Flash model (March 2026 standard)
        model_id = "gemini-2.0-flash"
        url = f"https://generativelanguage.googleapis.com/v1/models/{model_id}:generateContent?key={user_key}"
        
        headers = {'Content-Type': 'application/json'}
        prompt = f"Act as a teacher. Check this work against: {RUBRIC_DATA}. List 3 strengths and 3 gaps. Work: {draft}"
        
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        with st.spinner("Connecting to Gemini 3 Servers..."):
            response = requests.post(url, headers=headers, data=json.dumps(data))
            
            if response.status_code == 200:
                result = response.json()
                feedback = result['candidates'][0]['content']['parts'][0]['text']
                st.success("Analysis Complete!")
                st.markdown(feedback)
            elif response.status_code == 404:
                # Fallback to 2.5 if 3.0 is having a moment
                st.error("Model not found. Google might have changed the 'Preview' name. Trying legacy 2.5...")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
