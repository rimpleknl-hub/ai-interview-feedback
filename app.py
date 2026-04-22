import streamlit as st
import os
from openai import OpenAI
from docx import Document

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Interview Feedback", layout="centered")

# ---------- TITLE ----------
st.title("AI Interview Feedback Assistant 🤖")

# ---------- API ----------
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("API key not found. Please set it in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)
# ---------- FUNCTION: READ WORD FILE ----------
def read_docx(file):
    doc = Document(file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

# ---------- FUNCTION: AI ----------
def generate_feedback(transcript):
    prompt = f"""
You are an experienced and unbiased interviewer.

Analyze the following interview transcript and generate structured feedback.

IMPORTANT INSTRUCTIONS:
- Do not consider candidate’s region, gender, city, or background.
- Focus only on skills, communication, and responses.
- Be fair, objective, and consistent.
- Do not assume extra information.
- Ensure scoring is consistent across multiple runs for the same input.

OUTPUT FORMAT:

Summary:
(2-3 lines summary of candidate performance)

Overall Score:
(Give a score out of 10)

Skill-wise Ratings:
- Manual Testing: (Score out of 5 with 1 line reason)
- API Testing: (Score out of 5 with 1 line reason)
- Automation: (Score out of 5 with 1 line reason)
- Communication: (Score out of 5 with 1 line reason)

Strengths:
- Point 1
- Point 2
- Point 3

Areas of Improvement:
- Point 1
- Point 2
- Point 3

Red Flags:
- Mention any concerns or risks (or write "None")

Final Hiring Decision:
Decision: (Hire / No Hire / Consider)
Reason: (2-3 lines justification)

Interview Transcript:
{transcript}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


# ---------- OPTIONS ----------
st.subheader("Choose Input Method")

option = st.radio("Select option:", ["Upload File", "Use Sample Data"])

transcript = ""

# ---------- FILE UPLOAD ----------
if option == "Upload File":
    uploaded_file = st.file_uploader("Upload transcript (.txt or .docx)", type=["txt", "docx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".txt"):
            transcript = uploaded_file.read().decode("utf-8")

        elif uploaded_file.name.endswith(".docx"):
            transcript = read_docx(uploaded_file)

        st.success("File uploaded successfully ✅")

# ---------- SAMPLE ----------
elif option == "Use Sample Data":
    if st.button("Load Sample Transcript"):
        transcript = """Interviewer: Explain OOP concepts  
Candidate: Explained clearly with examples  
Interviewer: Any challenges?  
Candidate: Discussed debugging experience"""
        st.success("Sample loaded ✅")

# ---------- GENERATE ----------
if st.button("Generate Feedback"):
    if transcript.strip() == "":
        st.warning("Please upload or load transcript first")
    else:
        with st.spinner("Generating feedback..."):
            result = generate_feedback(transcript)

        st.success("Feedback Generated ✅")

        st.subheader("AI Generated Feedback")
        st.write(result)

        st.download_button(
            label="Download Feedback",
            data=result,
            file_name="interview_feedback.txt",
            mime="text/plain"
        )

# ---------- FOOTER ----------
st.markdown("---")
st.caption("AI-powered interview assistant")
