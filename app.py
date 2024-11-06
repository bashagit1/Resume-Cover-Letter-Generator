import streamlit as st
import os
from openai import OpenAI

# Set up OpenAI API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit app setup
st.set_page_config(page_title="Resume & Cover Letter Generator", page_icon="📝", layout="wide")

# Style customizations
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f7f7f7;
    }
    h1 {
        color: #2c3e50;
    }
    h2 {
        color: #2980b9;
    }
    .input-container {
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar with options
st.sidebar.markdown("<h2>🛠️ Options Panel</h2>", unsafe_allow_html=True)
resume_template = st.sidebar.selectbox("📄 Select Resume Template", ["Simple", "Professional", "Creative"])
cover_letter_style = st.sidebar.selectbox("💌 Cover Letter Style", ["Formal", "Informal", "Persuasive"])

# Main title
st.markdown("<h1 style='text-align: center;'>Resume & Cover Letter Generator 🌟</h1>", unsafe_allow_html=True)

# User input for personal information
st.markdown("<h3>📥 Enter Your Details:</h3>", unsafe_allow_html=True)

# Collapsible input sections
with st.expander("Personal Information"):
    name = st.text_input("👤 Full Name", placeholder="John Doe")
    email = st.text_input("📧 Email Address", placeholder="john.doe@example.com")
    phone = st.text_input("📞 Phone Number", placeholder="(123) 456-7890")

with st.expander("Work Experience"):
    experience = st.text_area("💼 Work Experience", placeholder="Describe your work experience...")

with st.expander("Education"):
    education = st.text_area("🎓 Education", placeholder="Your education details...")

with st.expander("Skills"):
    skills = st.text_area("🛠️ Skills", placeholder="List your skills...")

# Functions for OpenAI requests
def generate_resume():
    prompt = f"""
    Create a {resume_template.lower()} resume for {name} with the following details:
    Email: {email}
    Phone: {phone}
    Work Experience: {experience}
    Education: {education}
    Skills: {skills}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_cover_letter():
    prompt = f"""
    Write a {cover_letter_style.lower()} cover letter for {name} applying for a job. 
    The letter should include their email: {email}, phone: {phone}, 
    work experience: {experience}, education: {education}, and skills: {skills}.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Generate Resume and Cover Letter
if st.button("📝 Generate Resume"):
    if name and email and experience:
        resume = generate_resume()
        st.markdown("<h3>📄 Generated Resume:</h3>", unsafe_allow_html=True)
        st.write(resume)
        st.download_button(label="💾 Download Resume", data=resume, file_name="resume.txt")
    else:
        st.warning("Please fill in your details to generate a resume.")

if st.button("💌 Generate Cover Letter"):
    if name and email and experience:
        cover_letter = generate_cover_letter()
        st.markdown("<h3>💌 Generated Cover Letter:</h3>", unsafe_allow_html=True)
        st.write(cover_letter)
        st.download_button(label="💾 Download Cover Letter", data=cover_letter, file_name="cover_letter.txt")
    else:
        st.warning("Please fill in your details to generate a cover letter.")

# User guide
st.info("""### How to Use:
1. **Enter your personal details.**
2. **Select a template for your resume and style for your cover letter.**
3. **Click the buttons to generate your resume or cover letter.**
""")
