import streamlit as st
import requests
from streamlit_lottie import st_lottie
from style import add_background_color

st.set_page_config("VidQ", ":tada:", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_watching_video = load_lottieurl("https://lottie.host/873b2028-69e9-41cb-bc9b-55600d9c256e/Yt0acgMsbD.json")
video_url = ''

st.session_state["prev_url"] = ""

# Initialize session state for buttons and input
if "summary_clicked" not in st.session_state:
    st.session_state["summary_clicked"] = False
if "chat_clicked" not in st.session_state:
    st.session_state["chat_clicked"] = False
if "user_question" not in st.session_state:
    st.session_state["user_question"] = None
if "llm_answer" not in st.session_state:
    st.session_state["llm_answer"] = None


# Callback functions for buttons
def get_summary():
    st.session_state["summary_clicked"] = True
    st.session_state["chat_clicked"] = False  # Reset chat state


def start_chat():
    st.session_state["chat_clicked"] = True
    st.session_state["summary_clicked"] = False  # Reset summary state


def fetch_llm_answer(question):
    # Simulating an LLM response
    return f"Answer to '{question}': This is a simulated answer from the LLM."


# Layout
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
        url_input = st.text_input("Enter Podcast URL")
        submit_button = st.form_submit_button(label='Submit')

# Store video URL from the form
if submit_button:
    if url_input:
        try:
            video_url = url_input
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a valid URL.")

# Display the video, buttons, and handle button clicks
if video_url or st.session_state["prev_url"]:
    video_url = st.session_state.get("prev_url") if st.session_state.get("prev_url") else video_url
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)

        # Display the video in the left column
        with left_column:
            if video_url:
                st.video(video_url)
            elif video_url is '' and url_input:
                st.video(url_input)

        # Display buttons in the right column
        with right_column:
            st.markdown('<div class="button-container">', unsafe_allow_html=True)
                
            col1, col2 = st.columns([1, 1])

            with col1:
                st.button("Get Summary", on_click=get_summary)
                st.session_state["prev_url"] = video_url

            with col2:
                st.button("Chat", on_click=start_chat)

            st.markdown('</div>', unsafe_allow_html=True)

        # Handle Get Summary: Show the summary text below the buttons
        if st.session_state["summary_clicked"]:
            with right_column:
                st.write("Fetching video summary...")
                summary = "This is a brief summary of the video content."
                st.write(summary)

        # Handle Chat: Show input field for question and LLM response
        if st.session_state["chat_clicked"]:
            with right_column:
                st.write("Start chatting with the video content.")
                
                # Input field for user question
                question = st.text_input("Ask a question about the video:")

                # Store user question and fetch answer when submitted
                if st.button("Submit Question"):
                    if question:
                        st.session_state["user_question"] = question
                        st.session_state["llm_answer"] = fetch_llm_answer(question)
                    else:
                        st.warning("Please enter a question.")

                # Display the question and the LLM's response
                if st.session_state["user_question"]:
                    st.write(f"**Question:** {st.session_state['user_question']}")
                    if st.session_state["llm_answer"]:
                        st.write(f"**Answer:** {st.session_state['llm_answer']}")
