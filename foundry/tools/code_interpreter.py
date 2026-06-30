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
    model="gpt-5.1-mini",
    instructions="You are an AI assistant that provides information. Use the python tool to run code for math problems.",
    input="What is the square root of 16 ?",
    tools=[{
            "type": "code_interpreter", 
            "container": 
                {
                    "type": "auto"
                }
         }]
)

print(response.output_text)