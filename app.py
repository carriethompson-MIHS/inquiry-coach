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
        
       # --- THE TWO-PASS MASTER PROMPT ---
        rubric = """
      Analyze the student work in TWO distinct passes:

        PASS 1: EVALUATIVE RUBRIC STATUS
        For each of the 6 categories below, provide a brief 1-2 sentence evaluation of the current state of the work (even if it's just a snippet):
        - Claim & Reasoning
        - Depth of Inquiry
        - Organization & Structure
        - Academic Voice
        - Graphics & Visuals
        - Conventions

        PASS 2: TARGETED SKILL COACHING (Deep Dive)
        Provide specific, actionable guidance on these three "Exceeds Expectations" criteria:

        1. ORGANIZATION & FLOW: 
           - Is the writing organized with a synthesis of data and commentary? 
           - Are topic sentences and transitions strengthening the flow?
           - Identify one specific spot that needs better "Synthesis Language."

        2. INQUIRY DEPTH & DATA BALANCE:
           - Check for evidence of 15+ sources and a balance of Qualitative vs. Quantitative data.
           - Suggest what specific *type* of source or data is missing from this section.

        3. CLAIM & COUNTERCLAIM DEVELOPMENT:
           - Is the intro presenting info as 'relevant and critical'?
           - Does it distinguish the claim from opposing views and develop that counterclaim *thoroughly*?

        STRICT RULE: Do not rewrite the student's work. Use Socratic questioning to push them toward the 'Exceeds' category.
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

# --- FOOTER / VERSIONING ---
st.divider()
st.caption("Senior Inquiry Coach | Version 2.1 (Two-Pass Evaluator)")
st.caption("Last Updated: March 2026 | Built for MIHS Senior Inquiry")
