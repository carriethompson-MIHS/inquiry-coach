import streamlit as st
import google.generativeai as genai

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
st.info("Paste your work below to get feedback based on the 100-point rubric.")

# --- 3. THE SECRET KEY LOGIC ---
# This looks for a "Secret" named MY_API_KEY in the Streamlit Cloud settings.
if "MY_API_KEY" in st.secrets:
    user_key = st.secrets["MY_API_KEY"]
else:
    # If you're running this on your laptop, it will show this box instead.
    user_key = st.sidebar.text_input("Teacher/Admin API Key:", type="password")

# --- 4. THE INPUTS ---
mode = st.radio("Phase of Project:", ["Building the Outline", "Writing the Full Paper"])
draft = st.text_area("Paste your text here:", height=300, placeholder="Start typing or paste your draft...")

# --- 5. THE BRAIN ---
if st.button("Analyze My Work"):
    if not user_key:
        st.error("API Key not found. Please check Streamlit Secrets or enter it in the sidebar.")
    elif not draft:
        st.warning("Please paste some text first!")
    else:
        try:
            genai.configure(api_key=user_key)
            # Using the 2026 stable model name
            model = genai.GenerativeModel('gemini-2.0-flash-lite')
            
            if mode == "Building the Outline":
                phase_context = "The student is OUTLINING. Check for 15 source slots and logical flow."
            else:
                phase_context = "The student has a FULL DRAFT. Check strictly for 'I/Me/We' and MLA formatting."

            prompt = f"{phase_context} Rules: {RUBRIC_DATA}. List 3 Strengths, 3 Gaps, and 3 Revision Questions. Do not rewrite their work."
            
            with st.spinner("Analyzing..."):
                response = model.generate_content(prompt + "\n\nWork:\n" + draft)
                st.success("Analysis Complete!")
                st.markdown("### 📋 Coach's Feedback")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
