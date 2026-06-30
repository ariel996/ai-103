import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

project_name = os.getenv("project_name")
resource_name = os.getenv("resource_name")

project_endpoint = f"https://{resource_name}.services.ai.azure.com/api/projects/{project_name}"

project = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
)

openai_client = project.get_openai_client()

completions = openai_client.chat.completions.create(
    model="gpt-5.1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that answers questions and provides information."},
        {"role": "user", "content": "what is the capital of France ?"}
    ]
)

print(completions.choices[0].message.content)