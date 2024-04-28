from openai import OpenAI
import os
import json


organization_id = os.environ.get('ORGANIZATION_ID') # FIXME: if this doesnt work set your organization id environment variable
client = OpenAI(organization=organization_id)

INSTRUCTIONS = "You are a health and wellbeing assistant. Your job is to take in medical data about your patient, figure out the most relevant information to their current issue, and offer thoughtful responses on how to help them."

def main():
    # data_message = json_to_message("sample.json")
    assistant = make_assistant()
    thread = client.beta.threads.create()

    run_prompt(assistant, thread)
    # rp(assistant, thread)
    return 0

# def json_to_message(json):
#     with open(json, 'r') as file:
#         data = json.load(file)
    

def run_prompt(assistant, thread):  
    get_line(thread)
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            print(text)
            break

    return 0

# def rp(assistant, thread):
#     get_line(thread)
#     completion = client.chat.completions.create(
#         messages= thread.messages
#         assistant = assistant
#     )
#     print(completion.choices[0].message)

# When backend is invoked, do the following:

# Create a thread
    # Feed it messages.json
    # Feed it the Assistant

# Call Run on the thread
# Update messages.json

def get_line(thread):
    # read the user inputs from the terminal
    user_input = input("Enter a line: ")
    create_message(thread, user_input)
    return

# Give the AI its role/system and content
def make_assistant():
    assistant = client.beta.assistants.create(
        name = "Health Assistant",
        instructions = INSTRUCTIONS,
        model = "gpt-3.5-turbo",
        tools = [{"type": "file_search"}] # FIXME: add support to input files like context jsons, medical pdf
    )
    return assistant

def create_message(thread, message: str):
    client.beta.threads.messages.create(
        thread_id = thread.id,
        role="user",
        content = message
    )
    return



# Receive Prompt from User
# Receive data from context JSON
    # Read in a context json (all of the medical context from the apple watch)
        # turn it into a dictionary
        # turn the context into a messages() object 
            # assign role and content to each message()
            # parse the data and send it in as content
# Generate a response
# Store the response in message history JSON
# Send reponse back to the frontend

if __name__ == "__main__":
    main()