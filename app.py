import streamlit as st
from main import helper

st.set_page_config(page_title="Sirex Medical Assistant", page_icon="🏥")
st.title("🏥 Sirex Medical Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a medical question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = helper(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
