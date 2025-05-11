import os
from dotenv import load_dotenv
import openai
import streamlit as st

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ————————————————
# Streamlit UI
st.set_page_config(page_title="JobLens AI", page_icon="📝")
st.title("📝 JobLens AI")
st.markdown(
    """
    **Automatically rewrite your resume, cover letter, and LinkedIn summary**  
    Tailored to any job description using GPT-4.
    """
)

# Text inputs
job_desc = st.text_area("1. Paste the **Job Description** here:", height=200)
resume   = st.text_area("2. Paste your **Current Resume** here:", height=200)

# Action button
if st.button("👉 Rewrite Resume"):
    if not job_desc or not resume:
        st.error("Please provide both a job description and a resume.")
    else:
        with st.spinner("Generating your tailored resume…"):
            prompt = (
                "You are an expert career coach. Rewrite the resume below to perfectly "
                "match this job description, optimizing for ATS and personalization.\n\n"
                f"Job Description:\n{job_desc}\n\n"
                f"Resume:\n{resume}\n\n"
                "Output only the rewritten resume."
            )

            resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1600
            )

            rewritten = resp.choices[0].message.content.strip()
            st.subheader("✅ Rewritten Resume")
            st.write(rewritten)
            st.download_button(
                "💾 Download as Text File",
                data=rewritten,
                file_name="rewritten_resume.txt",
                mime="text/plain"
            )
