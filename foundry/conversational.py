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

response1 = openai_client.responses.create(
    model="gpt-5.4",
    instructions="You are a helpful AI assistant that explains technology concepts clearly.",
    input="What is machine learning ?"
)

print("Assistant: ", response1.output_text)

response2 = openai_client.responses.create(
    model="gpt-5",
    instructions="You are a helpful AI assistant that explains technology concepts clearly.",
    input="Can you give me an example ?",
    previous_response_id=response1.id
)

print("Assistant: ", response2.output_text)