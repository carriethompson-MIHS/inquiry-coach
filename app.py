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

# --- 4. THE BRAIN (DIRECT WEB REQUEST) ---
if st.button("Analyze My Work"):
    if not user_key:
        st.error("API Key missing!")
    elif not draft:
        st.warning("Please paste some text.")
    else:
        # This URL is the "Direct Line" that bypasses the v1beta error
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={user_key}"
        
        headers = {'Content-Type': 'application/json'}
        
        prompt = f"Act as a teacher. Check this work against: {RUBRIC_DATA}. List 3 strengths and 3 gaps. Work: {draft}"
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        with st.spinner("Talking directly to Google..."):
            response = requests.post(url, headers=headers, data=json.dumps(data))
            
            if response.status_code == 200:
                result = response.json()
                # Extracting the text from the complex Google response
                feedback = result['candidates'][0]['content']['parts'][0]['text']
                st.success("Analysis Complete!")
                st.markdown(feedback)
            elif response.status_code == 429:
                st.error("Google is busy (Quota Limit). Wait 60 seconds and try again!")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
