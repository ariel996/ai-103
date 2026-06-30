import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

resource_name = os.getenv("resource_name")
project_name = os.getenv("project_name")
AGENT_NAME = "ariel-code"

PROJECT_ENDPOINT = f"https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

agent = project.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful assistant that answers general questions"
    )
)

print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")