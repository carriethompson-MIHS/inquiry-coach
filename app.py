import streamlit as st
import requests
import json

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="ADMIN: Senior Inquiry Coach", layout="centered")

# --- 2. THE SIDEBAR (Admin Controls) ---
st.sidebar.header("🔑 Admin Settings")
api_key = st.sidebar.text_input("Paste API Key here:", type="password")
st.sidebar.info("This key powers the analysis. Get one at aistudio.google.com")

st.title("🎓 Senior Inquiry Feedback Coach")
st.subheader("Teacher/Admin Mode")

with st.expander("📝 Grading Rubric Overview"):
    st.write("""
    - **Claim & Reasoning (20pts):** Precise, engaged, distinguished.
    - **Depth of Inquiry (20pts):** 15+ sources, qualitative/quantitative balance.
    - **Organization (20pts):** Synthesis language, logical flow.
    - **Voice (15pts):** NO first/third person, active voice.
    - **Graphics (10pts):** Professional embedding, MLA formatting.
    - **Conventions (15pts):** Syntax variety, no run-ons, MLA citations.
    """)

# --- 3. THE INPUTS ---
mode = st.radio("Current Phase:", ["Building the Outline", "Writing the Full Paper"])
draft = st.text_area("Paste student work here:", height=300)

# --- 4. THE BRAIN ---
if st.button("Run Full Analysis"):
    if not api_key:
        st.error("Please paste your API Key in the sidebar to begin.")
    elif not draft:
        st.warning("Please paste student text to analyze.")
    else:
        model_id = "gemini-2.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1/models/{model_id}:generateContent?key={api_key}"
        
        # --- THE MASTER RUBRIC ---
        rubric = """
        Act as an expert Senior Inquiry Teacher. Analyze this work against these criteria:
        1. CLAIM & REASONING (20 pts): Precision of claim and engagement.
        2. DEPTH OF INQUIRY (20 pts): Evidence of 15+ sources and data balance.
        3. ORGANIZATION (20 pts): Synthesis language and paragraph flow.
        4. VOICE (15 pts): Absolute prohibition of first/third person (I, me, my, we, us) and passive voice.
        5. GRAPHICS (10 pts): Look for mentions/headers for visuals (MLA style).
        6. CONVENTIONS (15 pts): Sentence construction and MLA formatting.
        
        FORMAT: Use bold headers for categories. Provide 'Strengths' and 'Targeted Growth' for each.
        """

        prompt = f"{rubric}\n\nPHASE: {mode}\n\nWORK TO ANALYZE:\n{draft}"
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        with st.spinner("Analyzing against the 100-point rubric..."):
            try:
                response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
                if response.status_code == 200:
                    feedback = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("Analysis Complete!")
                    st.markdown(feedback)
                    
                    st.download_button(
                        label="📥 Download Teacher Copy",
                        data=feedback,
                        file_name="Teacher_Admin_Feedback.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"Google error: {response.json()['error']['message']}")
            except Exception as e:
                st.error(f"Error: {e}")
