from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_readme(project_context, api_key):
    """
    Generates a README.md file content using an AI model.
    """
    prompt_template = ChatPromptTemplate.from_template(
        "You are an expert technical writer specializing in creating beautiful, clear, and comprehensive README.md files.\n"
        "Based on the following complete project context, which includes file paths and their contents, generate an attractive and dynamic README.md file.\n\n"
        "The README should include:\n"
        "1. An engaging project title.\n"
        "2. A concise one-liner description.\n"
        "3. Project Structure"
        "4. A 'Key Features' section using bullet points.\n"
        "5. A 'Technologies Used' section.\n"
        "6. Clear 'Installation' and 'Usage' instructions based on the files (e.g., requirements.txt, package.json).\n"
        "7. If it's a web service, document the API endpoints you find.\n\n"
        "Here is the project context:\n\n"
        "```\n{context}\n```"
    )

    llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")
    chain = prompt_template | llm | StrOutputParser()
    
    print("🤖 AI is analyzing the project and writing the README...")
    readme_content = chain.invoke({"context": project_context})
    return readme_content