import streamlit as st
from streamlit_lottie import st_lottie
from server import get_response_from_query, get_transcript

import os
from dotenv import load_dotenv

from util import load_lottieurl

load_dotenv()
api_key = os.environ['OPENAI_API_KEY']

st.set_page_config("VidQ", ":tada:", layout="wide")

lottie_watching_video = load_lottieurl("https://lottie.host/873b2028-69e9-41cb-bc9b-55600d9c256e/Yt0acgMsbD.json")

if "messages" not in st.session_state:
        st.session_state.messages = []

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.title("VidQ")
        st.subheader("Ask Questions from Videos")
        st.write("Simple and quick way to understand the content of long videos.")
    with right_column:
        st_lottie(lottie_watching_video, height=250, key="watching_video")

# Video URL form
with st.container():
    st.write("---")
    st.header("Favorite Podcasts")
    with st.form(key='url_form'):
        st.session_state.url_input = ""
        url_input = st.text_input("Enter Podcast URL")
        st.session_state.url_input = url_input
        submit_button = st.form_submit_button(label='Submit')

if submit_button:
    st.session_state.messages = []

# Store video URL from the form
if url_input:
    left_column, right_column = st.columns(2)
    with left_column:
        st.video(url_input)
    with right_column:
        try:
            db = get_transcript(url_input)
            prompt = st.chat_input("Ask question from the video")
            if prompt:
                
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                with st.chat_message("user"):
                    st.markdown(prompt)
                
                st.session_state.messages.append({"role": "user", "content": prompt})
                response, docs = get_response_from_query(db, prompt)
                with st.chat_message("assistant"):
                    st.markdown(response)

                st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.warning("Please enter a valid URL.")
