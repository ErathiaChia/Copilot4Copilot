import requests
import json
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()


chat_history = []

# System prompt
system_prompt = """
    You are assisting a user in making a decision.
    The user has provided the following user input based on the context provided.
    Based on the user input, provide a single recommendation based on the most appropriate choice from the context provided.
    Follow the instructions strictly below to provide the recommendation.

    # INSTRUCTION :
     [A] You do not need to explain any decision, simply provide the outcome.
     [B] The outcome should only be either a number choice (1 - 6) or a "yes / no" response.
     [C] The outcome should be a single word or number, not a sentence or phrase.
     [D] The outcome should be the most appropriate choice based on the user input.
     [E] You should not blaber or provide any additional information, just provide the outcome.

    # EXAMPLES :
        if the CHOICES are "1. ... , 2. ..., 3. ...", and the USER_INPUT is leaning towards "3. ...", simply provide the output "3"
        if the CHOICES are "1. ... , 2. ..., 3. ...", and the USER_INPUT is leaning towards "2. ...", simply provide the output "2"
        if the CHOICES are "(1/2/3/4/5/6)", and the USER_INPUT is leaning towards "2", simply provide the output "2"
        if the CHOICES are either "yes/no", and the USER_INPUT is not positive, simply provide the answer as "no".
        if the CHOICES are either "yes/no", and the USER_INPUT is "Yes, ...", simply provide the answer as "yes".
        if the CHOICES are either "yes/no", and the USER_INPUT is "no, ...", simply provide the answer as "no".
"""

# Ollama API query
def query_ollama(prompt, system_prompt=system_prompt, model="llama3.3:70B"):
    """
    Send a query to Ollama API and get the response
    """
    try:
        request_body = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        if system_prompt:
            request_body["system"] = system_prompt

        response = requests.post('http://localhost:11434/api/generate',
                               json=request_body)

        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('response', '')
        return None
    except json.JSONDecodeError as e:
        try:
            full_response = ""
            response_data = {}
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if 'response' in json_response:
                        full_response += json_response['response']
                    # Store metadata from the last chunk
                    response_data = json_response
            response_data['response'] = full_response
            return response_data
        except Exception as e:
            print(f"Error processing streaming response: {e}")
            return None
    except Exception as e:
        print(f"Error querying Ollama: {e}")
        return None

def query_azure_openai(prompt, system_prompt=system_prompt):
    try:
        # Get credentials from environment variables
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT').rstrip('/')
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')

        # Construct the correct URL
        url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
        print(f"Making request to: {url}")  # Debug print

        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }

        response = requests.post(url, headers=headers, json=payload)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        response.raise_for_status()

        response_data = response.json()
        return response_data['choices'][0]['message']['content']

    except requests.RequestException as e:
        print(f"Request Error: {str(e)}")
        return "Error: Failed to connect to Azure OpenAI"
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return "Error: Something went wrong"

def get_ai_recommendation(context, user_prompt, choices="", chat_history=chat_history):
    prompt = f"""
    CONTEXT: {context}
    CHOICES: {choices}
    USER_INPUT: {user_prompt}
    -----------------------------------
    CHAT_HISTORY: {chat_history}
    """

    recommendation = query_azure_openai(prompt)  # query_ollama(prompt)

    # Never append None to chat history
    if recommendation is None:
        recommendation = "Error: Unable to get recommendation"

    chat_history.append("Context: " + str(context))
    chat_history.append("Possible Outcome: " + str(choices))
    chat_history.append("User Input: " + str(user_prompt))
    chat_history.append("Recommendation for User: " + str(recommendation))
    print("LLM Response -> ", recommendation)
    return recommendation

# def decision_tree():
#     kickoff = """
#     Welcome to the Co-Pilot for Co-Pilot!\n
#     Answer the following questions to determine the appropriate solution for your client's needs.\n

#     What do your client want to do? What is the goal of the project?

#           1. Search and Q&A in document(s)
#           2. Visualize text as a table or presentation
#           3. Generate text in document(s)
#           4. Extract data from document(s)
#           5. Summarize content or analyze sentiment in document(s)
#           6. Compare documents

#     Explain your client's needs and we'll help you determine the best route to take. :
#     """
#     choice = get_ai_recommendation(kickoff)

#     if choice == "1":
#         many_docs = get_ai_recommendation("Do you want to search within many documents? (yes/no): ")
#         if many_docs == "yes":
#             storage = get_ai_recommendation("Where are the documents stored? (sharepoint/other): ")
#             if storage == "sharepoint":
#                 print_copilot()
#             else:
#                 persist_results = get_ai_recommendation("Do you need to prioritize searches or persist search results? (yes/no): ")
#                 if persist_results == "yes":
#                     print_custom_genai_solution()
#                 else:
#                     print_ask_your_document
#         else:
#             print_copilot()

#     elif choice == "2":
#         print_copilot()

#     elif choice == "3":
#         one_doc = get_ai_recommendation("Do your users want to generate 1 document at a time? (yes/no): ")
#         if one_doc == "yes":
#             print_copilot()
#         else:
#             standards = get_ai_recommendation("Must the output adhere to specific policies, standards, or include content moderation? (yes/no): ")
#             if standards == "yes":
#                 print_custom_genai_solution()
#             else:
#                 print_copilot()

#     elif choice == "4":
#         auto_extract = get_ai_recommendation("Do you want to automatically extract data from multiple documents? (yes/no): ")
#         if auto_extract == "yes":
#             print_customized_copilot()
#         else:
#             ms_word = get_ai_recommendation("Are the documents residing or generated in M365 or SharePoint? (yes/no): ")
#             if ms_word == "yes":
#                 store_output = get_ai_recommendation("Do you want to store the output of the extraction automatically? (yes/no): ")
#                 if store_output == "yes":
#                     print_copilot()
#                 else:
#                     print_custom_genai_solution()
#             else:
#                 print_copilot()

#     elif choice == "5":
#         print_custom_genai_solution()

#     elif choice == "6":
#         compare_docs = get_ai_recommendation("Do you want to compare documents at scale? (yes/no): ")
#         if compare_docs == "yes":
#             print_custom_genai_solution()
#         else:
#             persist_comparison = get_ai_recommendation("Does the outcome of the comparison need to be persisted? (yes/no): ")
#             if persist_comparison == "yes":
#                 print_custom_genai_solution()
#             else:
#                 print_copilot()

#     else:
#         print("Invalid choice. Please restart and try again.")

# Run the decision tree script
# decision_tree()