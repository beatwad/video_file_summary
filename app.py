import os
from uuid import uuid4
import streamlit as st
from dotenv import load_dotenv

from src.transcribe import transcribe_video
from src.llm import generate_summary

load_dotenv()


def main():
    st.set_page_config(page_title="Video Summarizer", page_icon="📝")
    st.title("Local Video Summarizer 📝")
    st.write("Upload an MP4 file to transcribe audio and generate a summary using AI.")

    # File uploader
    uploaded_file = st.file_uploader("Choose an MP4 video", type=["mp4"])

    if uploaded_file is not None:
        # Create a runtimes folder
        directory = os.path.join(os.getcwd(), "runtimes")
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Display video
        st.video(uploaded_file)

        # Add a toggle/slider for "Transcribe only"
        transcribe_only = st.toggle("Transcribe only (save to file)")

        # Update button text based on mode
        btn_label = "Transcribe Only" if transcribe_only else "Transcribe & Summarize"
        process_button = st.button(btn_label)

        if process_button:
            status_text = st.empty()
            progress_bar = st.progress(0)

            try:
                # 1. Save uploaded file to temp path
                status_text.text("Saving file...")
                runtime_id = str(uuid4())
                temp_file_path = os.path.join(directory, f"{runtime_id}.mp4")

                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                progress_bar.progress(20)

                # 2. Transcribe
                status_text.text(
                    "Extracting audio and transcribing (Whisper)... This may take a moment."
                )
                transcribed_text = transcribe_video(temp_file_path)

                st.subheader("Transcription Preview")
                with st.expander("Show raw text"):
                    st.text(
                        transcribed_text[:2000] + "..."
                        if len(transcribed_text) > 2000
                        else transcribed_text
                    )

                progress_bar.progress(60)

                if transcribe_only:
                    status_text.text("Saving transcription to file...")

                    # Define transcribed folder path
                    transcribed_dir = os.path.join(os.getcwd(), "transcribed")

                    # Create folder if it doesn't exist
                    if not os.path.exists(transcribed_dir):
                        os.makedirs(transcribed_dir)

                    # Get original filename without extension
                    base_name = os.path.splitext(uploaded_file.name)[0]
                    save_path = os.path.join(transcribed_dir, f"{base_name}.txt")

                    # Save text to file
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(transcribed_text)

                    progress_bar.progress(100)
                    status_text.text("Done!")
                    st.success(f"Transcription saved successfully to: {save_path}")

                else:
                    # 3. Summarize (Existing Logic)
                    status_text.text("Sending to LLM for summarization...")
                    if not os.getenv(
                        "llm_api_key"
                    ):  # Note: logic assumes llm_api_key env var name, check .env consistency
                        # Fallback check for LLM_API_KEY as used in README instructions
                        if not os.getenv("LLM_API_KEY"):
                            st.error("API Key not found in .env file!")
                            st.stop()

                    summary = generate_summary(transcribed_text)

                    progress_bar.progress(100)
                    status_text.text("Done!")

                    # 4. Show Result
                    st.subheader("Summary & Key Points")
                    st.markdown(summary)

                # Cleanup
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                print(e)
            finally:
                status_text.empty()


if __name__ == "__main__":
    main()
