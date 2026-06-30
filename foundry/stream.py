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

response = openai_client.responses.create(
    model="gpt-5.4",
    instructions="You are a helpful assistant",
    input="what is the capital of France ?",
    stream=True,
    temperature=0
)

for event in response:
    if event.type == "response.output_text.delta":
        print(event.delta, end="")
    elif event.type == "response.completed":
        response_id = event.response.id
