
import streamlit as st
from chatbot import build_index, answer_question

st.set_page_config(
    page_title="TechNova Support",
    page_icon="💬",
    layout="centered"
)

st.title("💬 TechNova Customer Support")
st.caption("Ask questions about our company policies and services.")

@st.cache_resource
def load_rag():
    return build_index()

try:
    with st.spinner("Loading company documents..."):
        model, index, chunks = load_rag()
except Exception as e:
    st.error(f"Could not load the RAG system: {e}")
    st.info(
        "Check that your documents folder contains TXT or PDF files "
        "and that the required Python packages are installed."
    )
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sources"):
            st.caption("Sources: " + ", ".join(message["sources"]))

question = st.chat_input("Ask a question about our company...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching company documents..."):
            try:
                answer, sources = answer_question(
                    question, model, index, chunks
                )

                st.markdown(answer)
                st.caption("Sources: " + ", ".join(sources))

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")
