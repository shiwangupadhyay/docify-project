import google.generativeai as genai
from openai import OpenAI
from .prompts import *
from .helper import _parse_project_init_response


class Generator:
    """
    A class-based interface for generating documentation, tests, Dockerfiles,
    GitHub Actions workflows, and project scaffolds using Google Gemini or OpenAI GPT models.
    """

    def __init__(self, api_key: str):
        """
        Initialize the DocifyAI instance with an API key.

        Args:
            api_key (str): API key for the respective AI provider.
        """
        self.api_key = api_key

    def _gemini_generate(self, system_prompt: str, user_prompt: str, context: str) -> str:
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"{system_prompt}\n\n{user_prompt}\n\n{context}"
        response = model.generate_content(prompt)
        return response.text

    def _openai_generate(self, system_prompt: str, user_prompt: str, context: str) -> str:
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_prompt}\n\n{context}"},
            ],
        )
        return response.choices[0].message.content

    def generate_readme_gemini(self, project_context: str) -> str:
        print("Docify-AI is analyzing the project and writing the DOCS...")
        return self._gemini_generate(readme_system_prompt, readme_user_prompt, project_context)

    def generate_readme_openai(self, project_context: str) -> str:
        print("Docify-AI is analyzing the project and writing the DOCS...")
        return self._openai_generate(readme_system_prompt, readme_user_prompt, project_context)

    def generate_test_gemini(self, project_context: str) -> str:
        print("Docify-AI is analyzing the project and writing the Tests...")
        return self._gemini_generate(test_system_prompt, test_user_prompt, project_context)

    def generate_test_openai(self, project_context: str) -> str:
        print("Docify-AI is analyzing the project and writing the tests...")
        return self._openai_generate(test_system_prompt, test_user_prompt, project_context)

    def generate_dockerfile_gemini(self, project_context: str) -> str:
        print("Docify-AI is analyzing the project and writing the Dockerfile...")
        return self._gemini_generate(docker_system_prompt, docker_user_prompt, project_context)

    def generate_dockerfile_openai(self, project_context: str) -> str:
        print("Docify-AI is analyzing the project and writing the Dockerfile...")
        return self._openai_generate(docker_system_prompt, docker_user_prompt, project_context)

    def generate_gha_gemini(self, project_context: str) -> str:
        print("Docify-AI is analyzing the project and writing the GitHub Actions workflow...")
        return self._gemini_generate(gha_system_prompt, gha_user_prompt, project_context)

    def generate_gha_openai(self, project_context: str) -> str:
        print("Docify-AI is analyzing the project and writing the GitHub Actions workflow...")
        return self._openai_generate(gha_system_prompt, gha_user_prompt, project_context)

    def generate_project_init_gemini(self, project_name: str) -> dict:
        print("Docify-AI is creating a new Python project scaffold...")
        content = self._gemini_generate(init_system_prompt, init_user_prompt, project_name)
        return _parse_project_init_response(content)

    def generate_project_init_openai(self, project_name: str) -> dict:
        print("Docify-AI is creating a new Python project scaffold...")
        content = self._openai_generate(init_system_prompt, init_user_prompt, project_name)
        return _parse_project_init_response(content)
    
    def generate_docstring_gemini(self, project_context: str) -> str:
        print("Docify-AI is adding docstrings with Gemini...")
        return self._gemini_generate(docstring_system_prompt, docstring_user_prompt, project_context)


    def generate_docstring_openai(self, project_context: str) -> str:
        print("Docify-AI is adding docstrings with OpenAI...")
        return self._openai_generate(docstring_system_prompt, docstring_user_prompt, project_context)
    
    def generate_notebook_gemini(self, project_context: str, dataset_context: str) -> str:
        print("Docify-AI is generating a Jupyter Notebook with Gemini...")
        return self._gemini_generate(
            notebook_system_prompt,
            notebook_user_prompt.format(
                project_context=project_context,
                dataset_context=dataset_context
            ),
            ""
        )

    def generate_notebook_openai(self, project_context: str, dataset_context: str) -> str:
        print("Docify-AI is generating a Jupyter Notebook with OpenAI...")
        return self._openai_generate(
            notebook_system_prompt,
            notebook_user_prompt.format(
                project_context=project_context,
                dataset_context=dataset_context
            ),
            ""
        )

    def generate_model_card_gemini(self, project_context: str, dataset_context: str) -> str:
        print("Docify-AI is generating a MODEL_CARD.md with Gemini...")
        return self._gemini_generate(
            model_card_system_prompt,
            model_card_user_prompt.format(
                project_context=project_context,
                dataset_context=dataset_context
            ),
            ""
        )

    def generate_model_card_openai(self, project_context: str, dataset_context: str) -> str:
        print("Docify-AI is generating a MODEL_CARD.md with OpenAI...")
        return self._openai_generate(
            model_card_system_prompt,
            model_card_user_prompt.format(
                project_context=project_context,
                dataset_context=dataset_context
            ),
            ""
        )

    def fix_json_gemini(self, broken_json_string: str) -> str:
        """Asks Gemini to fix a broken JSON string."""
        print("Attempting to fix JSON with Gemini...")
        return self._gemini_generate(
            system_prompt=json_fix_system_prompt,
            user_prompt=broken_json_string,
            context=""
        )

    def fix_json_openai(self, broken_json_string: str) -> str:
        """Asks OpenAI to fix a broken JSON string."""
        print("Attempting to fix JSON with OpenAI...")
        return self._openai_generate(
            system_prompt=json_fix_system_prompt,
            user_prompt=broken_json_string,
            context=""
        )


