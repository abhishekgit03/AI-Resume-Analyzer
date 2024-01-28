import google.generativeai as genai
import os
import streamlit as st
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from PyPDF2 import PdfFileReader, PdfFileWriter,PdfReader


from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key = gemini_api_key)
model = genai.GenerativeModel('gemini-pro')


def query_function(text):

    response = model.generate_content(f"""You are provided with the resume of a candidate.
    Analyse the given resume of the candidate including projects and education. Let the candidate know where he can improve.
    List 5 important points that the recruiter may ask after going through the resume mentioned below.
    Part 3: What categories of companies the candidate must target?
    Part 4: Generate a score based on how good the resume is

    Resume of the candidate:
    {text}
    """)
    return response.text

def main():
    
    st.title("Resume Analyser")

   
    file = st.file_uploader("Please choose a file")
    if file is not None:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text+= page.extract_text()
        print(text)
    if st.button("Analyse"):
            with st.spinner('Analysing...'):
                answer = query_function(text)
            st.text("Here is the analysis:")
            st.write(answer)

if __name__ == "__main__":
    main()
