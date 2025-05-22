
import os

from dotenv import load_dotenv
from Extractor import extract_text
import json
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


load_dotenv()



class ResumeDetails(BaseModel):
    name: str = Field(description="Full name of the candidate")
    email: str = Field(description="Candidate's email address")
    mobile_no: str = Field(description="Candidate's contact number")
    profile_summary: Optional[str] = Field(
        description="A brief summary of the candidate's profile"
    )
    skills: Optional[List[str]] = Field(
        description="List of technical and soft skills mentioned in the resume"
    )
    certifications: Optional[List[str]] = Field(
        description="List of certifications obtained by the candidate"
    )



prompt_template = PromptTemplate(
    input_variables=["resume_text"],
    template="""
    Extract structured information from the following resume text. Return the output in valid JSON format.
    
    **Fields to extract:**
    - Name
    - Email
    - Mobile Number
    - Profile Summary
    - Skills (list format)
    - Certifications (list format)
    
    **Resume Text:**  
    {resume_text}

    **Response Format (JSON):**
    {{
        "name": "Full Name",
        "email": "example@email.com",
        "mobile_no": "+1234567890",
        "profile_summary": "Brief description...",
        "skills": ["Skill1", "Skill2"],
        "certifications": ["Certification1", "Certification2"]
    }}
    """,
)



def extract_resume_details(text):

    prompt = prompt_template.format(resume_text=text)

    model = ChatOpenAI(model_name="gpt-4-turbo", temperature=0)

    response = model.invoke(prompt) 

    if not response or not response.content:
        print("Error: Empty response from AI model.")
        return None

    try:
        response_text = response.content.strip() 

        print("AI Response:", response_text)

        extracted_data = json.loads(response_text) 

        return ResumeDetails(**extracted_data) 
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e}")
        return None

file_path = r"C:\Users\Pratham\Downloads\basisVector\Resume1.1.pdf"
extracted_text = extract_text(file_path)

structured_output = extract_resume_details(extracted_text)

if structured_output:
    print(structured_output.json(indent=4))

if structured_output:
    print(json.dumps(structured_output, indent=4))
