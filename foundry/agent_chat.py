import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

resource_name = os.getenv("resource_name")
project_name = os.getenv("project_name")

PROJECT_ENDPOINT=f"https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"
AGENT_NAME="ariel-code"

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential()
)

openai = project.get_openai_client()

conversation = openai.conversations.create()

response = openai.responses.create(
    conversation=conversation.id,
    extra_body={"agent_reference": {"name:": AGENT_NAME, "type": "agent_reference"}},
    input="What is the size of France in square miles ?"
)

print(response.output_text)

response = openai.responses.create(
    conversation=conversation.id,
    extra_body={"agent_reference": {"name": AGENT_NAME, "type": "agent_reference"}},
    input="And What is the capital city ?"
)

print(response.output_text)