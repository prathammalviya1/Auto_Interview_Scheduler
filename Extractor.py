import os
import PyPDF2
from PyPDF2 import PdfReader


import docx


def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        page_count = len(pdf_reader.pages)
        extracted_text = ""
        for page_num in range(
            len(pdf_reader.pages)
        ):  
            extracted_text += pdf_reader.pages[page_num].extract_text() + "\n"
        return extracted_text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.txt for para in doc.paragraphs])


def extract_text(file_path):

    _, file_extention = os.path.splitext(file_path)
  
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_extention == ".docx":
        return extract_text_from_docx(file_path)
