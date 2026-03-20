import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Senior Inquiry Coach", layout="centered")

# --- 2. THE RUBRIC ---
RUBRIC_DATA = """
- 15+ informational sources required.
- NO first/third person (I, me, you, we, us, my).
- 3+ quality visuals (graphs/charts) required.
- MLA formatting throughout.
- Precise, knowledgeable claims only.
"""

st.title("🎓 Senior Inquiry Feedback Coach")

# --- 3. THE SECRET KEY LOGIC ---
if "MY_API_KEY" in st.secrets:
    user_key = st.secrets["MY_API_KEY"]
else:
    user_key = st.sidebar.text_input("Teacher API Key:", type="password")

# --- 4. THE INPUTS ---
mode = st.radio("Phase of Project:", ["Building the Outline", "Writing the Full Paper"])
draft = st.text_area("Paste your text here:", height=300)

# --- 5. THE BRAIN ---
if st.button("Analyze My Work"):
    if not user_key:
        st.error("API Key missing!")
    elif not draft:
        st.warning("Please paste some text.")
    else:
        try:
            # FORCE FIX: Force 'rest' transport and 'v1' API version
            genai.configure(api_key=user_key, transport='rest')
            
            # Using the absolute most basic model name
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Act as a teacher. Check this work against: {RUBRIC_DATA}. List 3 strengths and 3 gaps. Do not rewrite it."
            
            with st.spinner("Forcing connection to Stable V1..."):
                # This 'request_options' line is the ultimate override for the 404 error
                response = model.generate_content(
                    prompt + "\n\nWork: " + draft,
                    request_options=RequestOptions(api_version='v1')
                )
                
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Technical Error: {e}")
            st.info("If you still see 404, we will try one last trick with the Model Name.")
