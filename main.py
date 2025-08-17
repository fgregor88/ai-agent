import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.schemas import available_functions
from functions.call_function import call_function


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
    You are inside calculator app directory.
    """

    for i in range(20): 
        response = client.models.generate_content(
            model = model,
            contents = messages,
            config = types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
                )
        )

        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose=verbose)

                if not function_call_result.parts[0].function_response.response:
                    raise RuntimeError("Fatal: function call returned no response.")

                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(
                role="user",
                parts=[types.Part(text=f"{function_call_result.parts[0].function_response.response}")]
            ))

        else:
            # No function calls, just print the model's text response
            print(response.text)
            break


    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")

        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
