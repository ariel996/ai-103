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

vector_store = openai_client.vector_stores.create(name="policy-docs")
openai_client.vector_stores.files.upload_and_poll(
    vector_store_id=vector_store.id,
    file=open("expenses_policy.pdf", "rb")
)

response = openai_client.responses.create(
    model="gpt-5.1-mini",
    instructions="You are an AI assistant that provides information from HR policy documents.",
    input="What's the maximum amount I can claim for a taxi ride ?",
    tools=[{
            "type": "file_search", 
            "vector_store_ids": [vector_store.id]
         }],
    include=["file_search_call.results"]
)

print(response.output_text)