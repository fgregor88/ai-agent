import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file

def main():
    print("Hello from ai-agent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1]

    verbose = "--verbose" in sys.argv

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    model = "gemini-2.0-flash-001"

    #system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

    system_prompt = """
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_get_file_content,
            schema_run_python_file
        ]
    )

    response = client.models.generate_content(
        model = model,
        contents = messages,
        config = types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
            )
    )

    print(response.text)

    if len(response.function_calls) > 0:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")

        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
