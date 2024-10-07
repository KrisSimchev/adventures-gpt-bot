import json
import os
from prompts import assistant_instructions

def create_assistant(client):
    assistant_file_path = 'assistant.json'

    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            vector_store_id = assistant_data['vector_store_id']
            print("Loaded existing assistant ID.")
    else:
        vector_store = client.beta.vector_stores.create(name="Knowledge about Adventures.bg")
        vector_store_id=vector_store.id

        file_paths = ["Main page.docx", "FAQ.docx", "about us.docx", "My voucher.docx", "universal voucher.docx"]
        file_streams = [open(path, "rb") for path in file_paths]


        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
        )

        print("Vector store created!")
        print(file_batch.status)
        print(file_batch.file_counts)

        assistant = client.beta.assistants.create(
            instructions=assistant_instructions,
            model="gpt-4o",
            tools=[{
                "type": "file_search"
            }],
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        )

        with open(assistant_file_path, 'w') as file:
            IDs = {
                'assistant_id': assistant.id,
                'vector_store_id': vector_store_id
            }
            json.dump(IDs, file)

        assistant_id = assistant.id

    return assistant_id, vector_store_id
