import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

project_name = os.getenv("project_name")
resource_name = os.getenv("resource_name")
project_endpoint = f"https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"

openai_project = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)

openai_client = openai_project.get_openai_client()

last_response_id = None

while True:
    input_text = input('\nYou: ')
    if input_text.lower() == 'quit':
        print("Assistant: Goodbye !")
        break
    
    response = openai_client.responses.create(
                model="gpt-5.4",
                instructions="You are a helpful AI assistant that explains technology concepts clearly.",
                input=input_text,
                previous_response_id=last_response_id
                )
    assistant_text = response.output_text
    print("\nAssistant: ", assistant_text)
    last_response_id = response.id
