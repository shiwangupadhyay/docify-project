import google.generativeai as genai
from openai import OpenAI
from .prompts import *

def generate_readme_gemini(project_context, api_key):
    """
    Generates a README.md file content using the Google Gemini model.
    """
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"{readme_system_prompt}\n\n{readme_user_prompt}\n\n{project_context}"

    print("Docify-AI is analyzing the project and writing the DOCS...")
    
    response = model.generate_content(prompt)
    
    return response.text


def generate_readme_openai(project_context, api_key):
    """
    Generates a README.md file content using the OpenAI API (GPT model).
    """
    client = OpenAI(api_key=api_key)

    print("Docify-AI is analyzing the project and writing the DOCS...")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": readme_system_prompt},
            {"role": "user", "content": f"{readme_user_prompt}\n\n{project_context}"}
        ]
    )
    
    return response.choices[0].message.content

def generate_test_gemini(project_context, api_key):
    """
    Generates a test folder containing test modules using the Google Gemini model.
    """
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"{test_system_prompt}\n\n{test_user_prompt}\n\n{project_context}"

    print("Docify-AI is analyzing the project and writing the Tests...")
    
    response = model.generate_content(prompt)
    
    return response.text


def generate_test_openai(project_context, api_key):
    """
    Generates a test folder containing test modules using the OpenAI API (GPT model).
    """
    client = OpenAI(api_key=api_key)

    print("Docify-AI is analyzing the project and writing the tests...")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": test_system_prompt},
            {"role": "user", "content": f"{test_user_prompt}\n\n{project_context}"}
        ]
    )
    
    return response.choices[0].message.content
