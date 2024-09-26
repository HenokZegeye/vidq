import streamlit as st
def add_background_color(color):
    st.markdown(f"""
        <style>
        .button-container {{
            background-color: {color};
            padding: 20px;
            border-radius: 10px;
        }}
        .button-column {{
            display: inline-block;
            width: 45%;
            margin: 0 2%;
        }}
        </style>
    """, unsafe_allow_html=True)