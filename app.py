import streamlit as st
import requests

st.set_page_config(page_title="Document Q&A Bot", page_icon="📄")

st.title("📄 Document Q&A Bot")
st.write("Upload a PDF and ask questions about it.")

BACKEND_URL = "http://127.0.0.1:8000"

# --- Upload section ---
st.header("1. Upload a document")
uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

if uploaded_file is not None:
    if st.button("Upload & process"):
        with st.spinner("Reading and chunking your document..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            response = requests.post(f"{BACKEND_URL}/upload", files=files)

        if response.status_code == 200:
            data = response.json()
            st.success(f"Done! {data['filename']} processed into {data['num_chunks']} chunks.")
        else:
            st.error("Something went wrong uploading the file.")

st.divider()

# --- Question section ---
st.header("2. Ask a question")
question = st.text_input("Type your question here")

if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please type a question first.")
    else:
        with st.spinner("Thinking..."):
            response = requests.post(f"{BACKEND_URL}/query", json={"question": question})

        if response.status_code == 200:
            data = response.json()
            st.subheader("Answer")
            st.write(data["answer"])

            with st.expander("View source chunks used"):
                for i, chunk in enumerate(data["sources"]):
                    st.markdown(f"**Chunk {i+1}:**")
                    st.text(chunk)
        else:
            st.error("Something went wrong getting the answer.")