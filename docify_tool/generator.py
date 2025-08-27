import google.generativeai as genai
from openai import OpenAI
from .prompts import *
from .helper import _parse_project_init_response

# readme generator

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

# test generator

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

#  DOCKERFILE GENERATORS

def generate_dockerfile_gemini(project_context, api_key):
    """
    Generates a Dockerfile using Google Gemini.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"{docker_system_prompt}\n\n{docker_user_prompt}\n\n{project_context}"

    print("Docify-AI is analyzing the project and writing the Dockerfile...")

    response = model.generate_content(prompt)
    return response.text


def generate_dockerfile_openai(project_context, api_key):
    """
    Generates a Dockerfile using OpenAI GPT models.
    """
    client = OpenAI(api_key=api_key)

    print("Docify-AI is analyzing the project and writing the Dockerfile...")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": docker_system_prompt},
            {"role": "user", "content": f"{docker_user_prompt}\n\n{project_context}"}
        ]
    )
    return response.choices[0].message.content


#  GITHUB ACTIONS GENERATORS

def generate_gha_gemini(project_context, api_key):
    """
    Generates a GitHub Actions CI/CD workflow using Google Gemini.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"{gha_system_prompt}\n\n{gha_user_prompt}\n\n{project_context}"

    print("Docify-AI is analyzing the project and writing the GitHub Actions workflow...")

    response = model.generate_content(prompt)
    return response.text


def generate_gha_openai(project_context, api_key):
    """
    Generates a GitHub Actions CI/CD workflow using OpenAI GPT models.
    """
    client = OpenAI(api_key=api_key)

    print("Docify-AI is analyzing the project and writing the GitHub Actions workflow...")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": gha_system_prompt},
            {"role": "user", "content": f"{gha_user_prompt}\n\n{project_context}"}
        ]
    )
    return response.choices[0].message.content

# PROJECT INIT GENERATORS

def generate_project_init_gemini(project_name, api_key):
    """
    Generates an initial Python project scaffold using Google Gemini.
    Returns JSON-like dict of files.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"{init_system_prompt}\n\n{init_user_prompt} {project_name}"

    print("Docify-AI is creating a new Python project scaffold...")

    response = model.generate_content(prompt)
    return _parse_project_init_response(response.text)


def generate_project_init_openai(project_name, api_key):
    """
    Generates an initial Python project scaffold using OpenAI GPT models.
    Returns JSON-like dict of files.
    """
    client = OpenAI(api_key=api_key)

    print("Docify-AI is creating a new Python project scaffold...")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": init_system_prompt},
            {"role": "user", "content": f"{init_user_prompt} {project_name}"}
        ]
    )
    return _parse_project_init_response(response.choices[0].message.content)
