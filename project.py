 import streamlit as st
from PIL import Image
import base64
import os
import requests
from urllib.parse import urlparse
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
from google.generativeai import configure, GenerativeModel
import fitz  # PyMuPDF
import re
import pandas as pd


# Initialize session state for message history
if 'message_history' not in st.session_state:
    st.session_state.message_history = []

api_key = "AIzaSyBZLHy1cs8PXr5JxU_V4Y79hyfS_GVMxWU"

# Now use the api_key in your configure function
configure(api_key=api_key)

# Create a Generative Model instance (assuming 'gemini-pro' is a valid model)
model = GenerativeModel('gemini-pro')


# Function to download generated report
def download_generated_report(content, filename, format='txt'):
    extension = format
    temp_filename = f"{filename}.{extension}"
    with open(temp_filename, 'w') as file:
        file.write(content)
    with open(temp_filename, 'rb') as file:
        data = file.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/{format};base64,{b64}" download="{filename}.{format}">Download Report ({format.upper()})</a>'
    st.markdown(href, unsafe_allow_html=True)
    os.remove(temp_filename)


# Function to load Lottie animations
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to extract topic from prompt
def extract_topic(prompt):
    start_phrases = ["@codex", "codex", "@AuranoxAI"]
    for phrase in start_phrases:
        if prompt.lower().startswith(phrase):
            return prompt[len(phrase):].strip()
    return prompt.strip()

# Function to fetch YouTube videos
def fetch_youtube_videos(query):
    # Insert the YouTube API key directly into your code
    youtube_api_key = "AIzaSyDeS7IK-tqlpYN-vBIF0FViaDBFJwpmjW8"


    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 4,
        "key": youtube_api_key
    }
    response = requests.get(search_url, params=params)
    video_details = []
    if response.status_code == 200:
        results = response.json()["items"]
        for item in results:
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_details.append({
                "title": video_title,
                "url": video_url,
                "video_id": video_id
            })
    else:
        st.error(f"Failed to fetch YouTube videos. Status code: {response.status_code}")
    return video_details





def add_tech_styles():
    tech_css = """
    <style>
    body {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%);
        font-family: 'Roboto', sans-serif;
        color: #000000;
    }

    /* Futuristic headings with sleek style */
    h1, h2, h3, h4, h5, h6 {
        color: #000000;
        font-weight: bold;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }


    }

    /* h3 - Blue Glow */
    h3 {
        text-shadow: 0 0 10px rgba(0, 0, 255, 1), 0 0 20px rgba(0, 0, 255, 0.8);
        animation: glow-h3 1.5s ease-in-out infinite alternate;
    }

    /* h4 - Red and Yellow Glow */
    h4 {
        text-shadow: 0 0 10px rgba(255, 0, 0, 1), 0 0 20px rgba(255, 255, 0, 0.8);
        animation: glow-h4 1.5s ease-in-out infinite alternate;
    }

    /* h5 - Purple Glow */
    h5 {
        text-shadow: 0 0 10px rgba(128, 0, 128, 1), 0 0 20px rgba(128, 0, 128, 0.8);
        animation: glow-h5 1.5s ease-in-out infinite alternate;
    }

    /* h6 - Light Pink Glow */
    h6 {
        text-shadow: 0 0 10px rgba(255, 182, 193, 1), 0 0 20px rgba(255, 182, 193, 0.8);
        animation: glow-h6 1.5s ease-in-out infinite alternate;
    }

    /* Neon glow effect for buttons */
    .stButton button {
        background-color: #0f0f0f;
        border: 1px solid #00ffff;
        color: #00ffff;
        padding: 14px 28px;
        font-size: 16px;
        border-radius: 12px;
        transition: box-shadow 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.8), 0 0 20px rgba(0, 255, 255, 0.6);
    }

    .stButton button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 255, 1), 0 0 40px rgba(0, 255, 255, 0.8);
    }

    /* Glassmorphism cards */
    .static-middle {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        text-align: center;
        margin: 40px auto;
    }

    /* Input fields with tech-inspired look */
    input[type='text'], textarea {
        background-color: #1a1a1a;
        border: 1px solid #00ffff;
        color: #eaeaea;
        padding: 12px;
        font-size: 16px;
        border-radius: 8px;
    }

    input[type='text']:focus, textarea:focus {
        border-color: #00ffff;
        transition: border-color 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
    }



    /* Keyframes for glow effects */
    @keyframes glow-h1 {
        0% {
            text-shadow: 0 0 10px rgba(0, 255, 255, 1), 0 0 20px rgba(0, 255, 255, 0.8);
        }
        100% {
            text-shadow: 0 0 20px rgba(0, 255, 255, 1), 0 0 40px rgba(0, 255, 255, 0.8);
        }
    }

    @keyframes glow-h2 {
        0% {
            text-shadow: 0 0 10px rgba(0, 255, 0, 1), 0 0 20px rgba(0, 255, 0, 0.8);
        }
        100% {
            text-shadow: 0 0 20px rgba(0, 255, 0, 1), 0 0 40px rgba(0, 255, 0, 0.8);
        }
    }

    @keyframes glow-h3 {
        0% {
            text-shadow: 0 0 10px rgba(0, 0, 255, 1), 0 0 20px rgba(0, 0, 255, 0.8);
        }
        100% {
            text-shadow: 0 0 20px rgba(0, 0, 255, 1), 0 0 40px rgba(0, 0, 255, 0.8);
        }
    }

    @keyframes glow-h4 {
        0% {
            text-shadow: 0 0 10px rgba(255, 0, 0, 1), 0 0 20px rgba(255, 255, 0, 0.8);
        }
        100% {
            text-shadow: 0 0 20px rgba(255, 0, 0, 1), 0 0 40px rgba(255, 255, 0, 0.8);
        }
    }

    @keyframes glow-h5 {
        0% {
            text-shadow: 0 0 10px rgba(128, 0, 128, 1), 0 0 20px rgba(128, 0, 128, 0.8);
        }
        100% {
            text-shadow: 0 0 20px rgba(255, 0, 255, 1), 0 0 40px rgba(255, 0, 255, 0.8);
        }
    }

    @keyframes glow-h6 {
        0% {
            text-shadow: 0 0 10px rgba(255, 182, 193, 1), 0 0 20px rgba(255, 182, 193, 0.8);
        }
        100% {
            text-shadow: 0 0 20px rgba(255, 182, 193, 1), 0 0 40px rgba(255, 182, 193, 0.8);
        }
    }

    @keyframes divider-glow {
        0% {
            border-top-color: rgba(0, 255, 255, 0.5);
        }
        100% {
            border-top-color: rgba(0, 255, 255, 1);
        }
    }

    </style>
    """
    st.markdown(tech_css, unsafe_allow_html=True)





def main():
    st.set_page_config(page_title="Well Guardian", page_icon="🧠", layout="wide",
                       initial_sidebar_state="expanded")

    # Apply custom styles (LED lines and static middle section)
    add_tech_styles()
   
    # Add LED line at the top
    st.markdown('<div class="led-line"></div>', unsafe_allow_html=True)

    st.sidebar.image("", use_column_width=True)
    page = st.sidebar.selectbox("**MENU**",
                                ["♖ Introduction", "🧠 Wellness Mentor", "📝 Medical Report Analysis", "💊 Drug Details",
                                 "🧑‍⚕️ Expert Advice", "⚖️ Privacy Policy"])

    # Define background colors for each page
    background_colors = {
        "♖ Introduction": "#FFD700",  # Gold
        "🧠 Wellness Mentor": "#32CD32",  # Lime Green
        "📝 Medical Report Analysis": "#00BFFF",  # Deep Sky Blue
        "💊 Drug Details": "#FF6347",  # Tomato Red
        "🧑‍⚕️ Expert Advice": "#6A5ACD",  # Slate Blue
        "⚖️ Privacy Policy": "#FF69B4"   # Hot Pink
    }

    

    


  
    if page == "♖ Introduction":
        st.title("Welcome to Auranox AI 🧑‍⚕️")
        st.markdown("""
        **Auranox AI**:
        Auranox, powered by the Gemini API, is a basic application designed for Mental Health Care. 
        // Auranox - A blend of "aura" and "nox," signifying mental peace even in the darkest times.
        """)

        # Embedding Lottie animation
        lottie_url = "https://lottie.host/d7233830-b2c0-4719-a5c0-0389bd2ab539/qHF7qyXl5q.json"
        lottie_animation = load_lottie_url(lottie_url)
        if lottie_animation:
            st_lottie(lottie_animation, speed=1, width=400, height=300, key="lottie_animation")
        else:
            st.error("Failed to load Lottie animation.")

        st.markdown("""
        **Guidelines:**

        - **Respectful Conduct**: Users are expected to engage in respectful and considerate interactions within the Auranox community. Any form of harassment, hate speech, or derogatory behavior will not be tolerated.
        - **Accuracy of Information**: While Auranox aims to provide helpful information and support, users should understand that the content provided is for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for personalized guidance.
        - **Data Privacy**: Auranox respects user privacy and confidentiality. Personal information shared within the platform will be handled with the utmost care and will not be shared with third parties without explicit consent, except as required by law.
        - **Safety and Well-being**: Auranox prioritizes the safety and well-being of its users. If you or someone you know is in crisis or experiencing a medical emergency, please seek immediate assistance from a qualified healthcare professional or emergency services.

        Developed by Mahdi, we are more focused on creating practical AI projects, Auranox is intended for educational purposes only. We do not endorse any illegal or unethical activities.
        """)
    elif page == "🧠 Wellness Mentor":
        st.header("🧠 Wellness Mentor")
        # Initialize session state for message history
        if 'message_history' not in st.session_state:
            st.session_state.message_history = []

        lottie_url = "https://lottie.host/0c079fc2-f4df-452a-966b-3a852ffb9801/WjOxpGVduu.json"
        # Load and display Lottie animation
        lottie_animation = load_lottie_url(lottie_url)
        if lottie_animation:
            st_lottie(lottie_animation, speed=1, width=220, height=300, key="lottie_animation")
        else:
            st.error("Failed to load Lottie animation.")

        st.markdown(
            "Auranox may provide inaccurate responses. Read all the guidelines and usage instructions. Contact a doctor before proceeding.")

        question = st.text_input("Ask the model a question:")
        if st.button("Ask AI"):
            topic = extract_topic(question)

            with st.spinner("Loading brilliance... almost there! 😉"):
                try:
                    response = model.generate_content(f"You are an expert mental healthcare professional: {question}")
                    if response.text:
                        st.text("Auranox Response:")
                        st.write(response.text)
                        st.markdown('---')
                        
                        st.session_state.message_history.append({"question": question, "response": response.text})
                        st.subheader("Message History:")
                        with st.expander("View Message History", expanded=False):
                            for msg in st.session_state.message_history:
                                st.markdown(f"**You:** {msg['question']}")
                                st.markdown(f"**Auranox:** {msg['response']}")
                                st.markdown("---")

                        
                        # Fetch YouTube video suggestions
                        video_suggestions = fetch_youtube_videos(topic)
                        if video_suggestions:
                            st.markdown("### YouTube Video Suggestions:")

                            # Summary provided by the model
                            summary = response.text

                            # Display the summary
                            st.markdown(f"**Summary:** {summary}")

                            for video in video_suggestions:
                                st.write(f"[{video['title']}]({video['url']})")
                                st.video(video["url"])

                    else:
                        st.error("No valid response received from the AI model.")
                        st.write(f"Safety ratings: {response.safety_ratings}. Change the prompt to continue.")
                except ValueError as e:
                    st.info(f"🤐 Unable to assist with that prompt due to: {e}. Change the prompt to continue.")
                except IndexError as e:
                    st.info(f"🤐 Unable to assist with that prompt due to: {e}. Change the prompt to continue.")
                except Exception as e:
                    st.info(f"An unexpected error occurred 😕. Change the prompt to continue: {e}")

                report_keywords = ["report", "health", "illness", "summary", "sick"]
                if any(keyword in question.lower() for keyword in report_keywords):
                    if response.text:
                        download_generated_report(response.text, "report")
        if st.button("Clear History"):
            st.session_state.message_history.clear()
            st.success("Message history cleared.")
        
        st.markdown('---')

    elif page == "📝 Medical Report Analysis":
        st.header("📝 Medical Report Analysis")
        st.markdown("Upload your medical report (PDF format):")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if uploaded_file is not None:
            try:
                text = extract_text_from_pdf(uploaded_file)
                st.text_area("Extracted Text:", text, height=300)

                if st.button("Analyze Report"):
                    with st.spinner("Analyzing report..."):
                        try:
                            prompt = f"Analyze the following medical report and provide insights:\n\n{text}"
                            response = model.generate_content(prompt)
                            if response.text:
                                st.text("Analysis:")
                                st.write(response.text)
                                download_generated_report(response.text, "analysis", format="txt")
                            else:
                                st.error("No valid response received from the AI model.")
                        except ValueError as e:
                            st.error(f"Unable to analyze the report: {e}")
                        except IndexError as e:
                            st.error(f"Unable to analyze the report: {e}")
                        except Exception as e:
                            st.error(f"An unexpected error occurred while analyzing the report: {e}")

            except Exception as e:
                st.error(f"Failed to extract text from PDF: {e}")

    elif page == "💊 Drug Details":
        st.header("💊 Drug Details")
        st.markdown("Select the input method:")

        input_method = st.radio("Choose the input method:", ("Text Input", "PDF Upload"))

        if input_method == "Text Input":
            medicine_name = st.text_input("Enter the medicine name:")

            if st.button("Analyze Medicine"):
                with st.spinner("Analyzing medicine details..."):
                    try:
                        prompt = f"Provide insights on the following medicine: {medicine_name}"
                        response = model.generate_content(prompt)
                        if response.text:
                            st.text("Analysis:")
                            st.write(response.text)
                            download_generated_report(response.text, "medicine_analysis", format="txt")
                        else:
                            st.error("No valid response received from the AI model.")
                    except ValueError as e:
                        st.error(f"Unable to analyze the medicine details: {e}")
                    except IndexError as e:
                        st.error(f"Unable to analyze the medicine details: {e}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred while analyzing the medicine details: {e}")

        elif input_method == "PDF Upload":
            uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

            if uploaded_file is not None:
                try:
                    text = extract_text_from_pdf(uploaded_file)
                    st.text_area("Extracted Text:", text, height=300)

                    if st.button("Analyze Medicine"):
                        with st.spinner("Analyzing medicine details..."):
                            try:
                                prompt = f"Analyze the following medicine details and provide insights:\n\n{text}"
                                response = model.generate_content(prompt)
                                if response.text:
                                    st.text("Analysis:")
                                    st.write(response.text)
                                    download_generated_report(response.text, "medicine_analysis", format="txt")
                                else:
                                    st.error("No valid response received from the AI model.")
                            except ValueError as e:
                                st.error(f"Unable to analyze the medicine details: {e}")
                            except IndexError as e:
                                st.error(f"Unable to analyze the medicine details: {e}")
                            except Exception as e:
                                st.error(f"An unexpected error occurred while analyzing the medicine details: {e}")

                except Exception as e:
                    st.error(f"Failed to extract text from PDF: {e}")

    elif page == "🧑‍⚕️ Expert Advice":
        st.header("🧑‍⚕️‍Expert Advice")
        st.markdown("""
            **Available Experts:**

            - Dr. Graham Williams (Psychologist)
            - Dr. Karim Khalil (Psychiatrist)
            - Dr. Samira Alexander (Mental Health Counselor)
        """)

        contact_form = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Auranox AI</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #121212;
            color: #e0e0e0;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #1e1e1e;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            padding: 40px;
            width: 400px;
            box-sizing: border-box;
        }
        h1 {
            margin-bottom: 20px;
            text-align: center;
            color: #81c784;
        }
        label {
            display: block;
            margin-bottom: 10px;
            font-size: 14px;
            color: #81c784;
        }
        input[type="text"],
        input[type="email"],
        select,
        textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #333;
            border-radius: 4px;
            background-color: #2c2c2c;
            color: #ffffff;
            box-sizing: border-box;
        }
        input[type="text"]::placeholder,
        input[type="email"]::placeholder,
        textarea::placeholder {
            color: #888;
        }
        input[type="text"]:focus,
        input[type="email"]:focus,
        textarea:focus,
        select:focus {
            border-color: #81c784;
            outline: none;
        }
        textarea {
            height: 120px;
            resize: none;
        }
        button[type="submit"] {
            background-color: #81c784;
            color: #121212;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
            display: block;
            width: 100%;
        }
        button[type="submit"]:hover {
            background-color: #66bb6a;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Contact Auranox AI</h1>
        <form action="https://formspree.io/f/xqazvqor" method="POST">
            <label>
                Your name:
                <input type="text" name="name" placeholder="Enter your name" required>
            </label>
            <label>
                Your email:
                <input type="email" name="email" placeholder="Enter your email" required>
            </label>
            <label>
                Your message:
                <textarea name="message" placeholder="Enter your message" required></textarea>
            </label>
            <label>
                Mental health concern:
                <select name="concern" required>
                    <option value="" disabled selected>Select your concern</option>
                    <option value="anxiety">Anxiety</option>
                    <option value="depression">Depression</option>
                    <option value="stress">Stress</option>
                    <option value="relationship">Relationship Issues</option>
                    <option value="other">Want to Die</option>
                    <option value="other">Other</option>
                </select>
            </label>
            <button type="submit">Send</button>
        </form>
    </div>
</body>
</html>


        """
        st.markdown(contact_form, unsafe_allow_html=True)

    elif page == "⚖️ Privacy Policy":
        st.header("⚖️ Privacy Policy")
        st.markdown("""
        **Privacy Policy of Auranox AI**:

        At Auranox AI, we prioritize your privacy and are committed to protecting your personal information. This Privacy Policy outlines the types of information we collect, how we use and safeguard that information, and your rights regarding your data.

        **Information We Collect:**

        - **Personal Information:** When you register or use our services, we may collect personal information such as your name, email address, and contact details.
        - **Usage Data:** We collect information about your interactions with our platform, including the features you use, the pages you visit, and the actions you take.
        - **Cookies and Tracking Technologies:** We use cookies and similar tracking technologies to enhance your experience on our platform and gather information about your usage patterns.

        **How We Use Your Information:**

        - **To Provide Services:** We use your information to deliver our services, respond to your inquiries, and fulfill your requests.
        - **Improvement and Personalization:** We analyze usage data to improve our platform, personalize your experience, and develop new features.
        - **Communication:** We may use your contact information to send you updates, newsletters, and other relevant communications.

        **Data Security:**

        We implement industry-standard security measures to protect your data from unauthorized access, alteration, disclosure, or destruction. However, please note that no method of transmission over the internet or electronic storage is completely secure.

        **Your Rights:**

        - **Access and Correction:** You have the right to access and correct your personal information held by us.
        - **Data Deletion:** You can request the deletion of your personal information from our records.
        - **Opt-Out:** You can opt out of receiving marketing communications from us at any time.

        **Contact Us:**

        If you have any questions or concerns about our Privacy Policy or data practices, please contact us.

        **Changes to This Privacy Policy:**

        We may update this Privacy Policy from time to time to reflect changes in our practices or legal requirements. We will notify you of any significant updates.
        """)




if __name__ == "__main__":
    main()
