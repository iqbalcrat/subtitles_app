import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))


# Set up OpenAI API key


# Set up the Streamlit app
st.set_page_config(page_title="Subtitles generator", layout="wide")

# Sidebar content
with st.sidebar:
    st.write("Upload your audio file and click submit.")

# Main content
st.title("Audio Transcription App")

# Directory to save uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# File upload widget in the sidebar
uploaded_file = st.sidebar.file_uploader(
    "Upload an audio file", 
    type=["mp3", "wav", "ogg", "flac"], 
    accept_multiple_files=False
)

# Submit button
if st.sidebar.button("Submit"):
    if uploaded_file is not None:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"File '{uploaded_file.name}' uploaded and saved successfully!")
        st.audio(file_path, format="audio/mp3")  # Adjust format if needed

        # Transcription process
        try:
            audio_file= open(file_path, "rb")
            transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="srt"
            )
            print(transcription)
            # Display transcription in a text area
            st.subheader("Transcription")
            st.text_area("Generated Subtitles:", transcription, height=300)

            # Save transcription to an SRT file
            srt_file_path = os.path.join(UPLOAD_DIR, f"{os.path.splitext(uploaded_file.name)[0]}.srt")
            with open(srt_file_path, "w") as srt_file:
                srt_file.write(transcription)

            # Button to download subtitles
            with open(srt_file_path, "rb") as srt_file:
                st.download_button(
                    label="Download Subtitles",
                    data=srt_file,
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}.srt",
                    mime="text/srt"
                )
        except Exception as e:
            st.error(f"Error during transcription: {e}")
    else:
        st.error("Please upload an audio file before submitting.")
