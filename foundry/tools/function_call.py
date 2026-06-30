import time
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


def get_time():
    return f"The time is {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"


def main():
    openai_client = openai_project.get_openai_client()
    
    function_tools = [
        {
            "type": "function",
            "name": "get_time",
            "description": "Get the current time"
        }
    ]
    
    messages = [
        {"role": "developer", "content": "You are an AI assistant that provides information."}
    ]
    
    while True:
        prompt = input("\nEnter a prompt (or type 'quit' to exit)\n")
        if prompt.lower() == "quit":
            break
        
        messages.append({"role": "user", "content": prompt})

    response = openai_client.responses.create(
        model="gpt-5.1-mini",
        input=messages,
        tools=function_tools
    )
    
    messages += response.output
    
    for item in response.output:
        if item.type == "function_call" and item.name == "get_time":
            current_time = get_time()
            messages.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": current_time
            })
            
            response = openai_client.responses.create(
                model="gpt-5.1",
                instructions="Answer only with the tool output.",
                input=messages,
                tools=function_tools
            )

    print(response.output_text)
    
if __name__ == '__main__':
    main()