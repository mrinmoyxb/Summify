from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import tempfile
import streamlit as st

load_dotenv()

st.header("📚 Summify")
st.write("Summarize any text or document")

uploaded_file = st.file_uploader(label = "Upload your PDF", type="pdf", accept_multiple_files=False)
summary_length = st.selectbox(label = "Select summary length", options = [
    "Short(3 or 5 bullet points)", "Medium(1 or 2 paragraphs)", "Detailed(More than 2 paragraphs)"
])
summary_type = st.selectbox(label="Select summary type", options = ["Abstractive", "Extractive"])
summary_tone = st.selectbox(label="Select summary tone", options = ["Academic", "Casual", "Professional"])
summary_models = st.selectbox(label="Select model", options = ["Claude 3.5 Sonnet", "Gemini 1.5 pro", "Mistral-7B-Instruct-v0.2"])

prompt = PromptTemplate(
    template="""Summarize the given document: {uploaded_file} and must consider the following parameters:
    - summary length: {summary_length}
    - summary type: {summary_type}
    - summary tone: {summary_tone}
    """,
    input_variables=["uploaded_file", "summary_length", "summary_type", "summary_tone"]
)

if uploaded_file==None:
    st.write("Document is not available")
else:
    with tempfile.NamedTemporaryFile(delete = False, suffix = ".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name
        loader = PyPDFLoader(temp_path)
        pages = loader.load()
        paragraph = " ".join(pages[0].page_content.split())
        st.write(paragraph[0:1000]+"...")
        