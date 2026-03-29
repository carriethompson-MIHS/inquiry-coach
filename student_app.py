import streamlit as st
import requests
import json

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Senior Inquiry Coach", layout="centered")

# --- 2. STUDENT INSTRUCTIONS ---
st.title("🎓 Senior Inquiry Feedback Coach")
with st.expander("📖 READ THIS: Instructions for 11-15 Page Papers"):
    st.write("""
    **To get the best feedback, please paste 3-5 pages at a time.**
    * **Phase 1 (Outline):** Focuses on claim, reasoning, and planned depth of inquiry.
    * **Phase 2 (Full Paper):** Checks for voice, synthesis, MLA, and conventions.
    * *Note: The AI cannot "see" your images, so tell it where they are (e.g., "[Graph 1 here]") so it can check your formatting!*
    """)

# --- 3. THE INPUTS ---
mode = st.radio("What are we checking?", ["Building the Outline", "Writing the Full Paper"])
draft = st.text_area("Paste your work here:", height=300)

# --- 4. THE BRAIN (Hidden Key) ---
api_key = st.secrets["MY_API_KEY"]

if st.button("Analyze My Work"):
    if not draft:
        st.warning("Please paste some text first.")
    else:
        model_id = "gemini-2.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1/models/{model_id}:generateContent?key={api_key}"
        
        # --- THE MASTER RUBRIC ---
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

        prompt = f"{rubric}\n\nCURRENT PHASE: {mode}\n\nSTUDENT WORK:\n{draft}"
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        with st.spinner("Applying the Master Rubric..."):
            try:
                response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
                if response.status_code == 200:
                    feedback = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("Analysis Complete!")
                    st.markdown(feedback)
                    
                    st.download_button(
                        label="📥 Download Feedback Report",
                        data=feedback,
                        file_name="Senior_Inquiry_Feedback.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("The coach is busy. Wait 60 seconds and try again!")
            except Exception as e:
                st.error(f"Error: {e}")
