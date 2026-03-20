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
        Act as a high school Senior Inquiry teacher. Provide feedback based on these EXACT criteria:
        
        1. CLAIM & REASONING (20 pts): Does it powerfully engage the reader? Is the claim precise and distinguished from opposing claims?
        2. DEPTH OF INQUIRY (20 pts): Look for evidence of 15+ sources and a balance of qualitative/quantitative data.
        3. ORGANIZATION (20 pts): Look for synthesis language. Does each element build on the previous to create a unified whole? Are there topic sentences and transitions?
        4. VOICE (15 pts): Strictly NO first/third person (I, me, my, we, us) and NO passive voice. Use domain-specific vocabulary.
        5. GRAPHICS (10 pts): Check if the student has referred to visuals (e.g., "See Figure 1") per MLA format and used headers effectively.
        6. CONVENTIONS (15 pts): Check for sentence variety, MLA formatting, and lack of run-ons/fragments.
        
        OUTPUT FORMAT:
        - Give a brief 'Overall Impression'.
        - Break down feedback by the 6 categories above.
        - Use 'Strengths' and 'Targeted Improvements' for each.
        - Be supportive but academically rigorous.
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
