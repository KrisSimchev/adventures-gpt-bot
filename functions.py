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

        main_page_file = client.files.create(file=open("Main page.docx", "rb"),
                                        purpose='assistants')
        FAQ_file = client.files.create(file=open("FAQ.docx", "rb"),
                                        purpose='assistants')
        about_us_file = client.files.create(file=open("about us.docx", "rb"),
                                        purpose='assistants')
        my_voucher_file = client.files.create(file=open("My voucher.docx", "rb"),
                                        purpose='assistants')
        universal_voucher_file = client.files.create(file=open("universal voucher.docx", "rb"),
                                        purpose='assistants')

        main_page_file_id = main_page_file.id
        FAQ_file_id = FAQ_file.id
        about_us_file_id = about_us_file.id
        my_voucher_file_id = my_voucher_file.id
        universal_voucher_file_id = universal_voucher_file.id

        vector_store = client.beta.vector_stores.create(
            name="Knowledge about Adventures.bg",
            file_ids=[
                main_page_file_id, FAQ_file_id, about_us_file_id, my_voucher_file_id, universal_voucher_file_id
            ])

        vector_store_id = vector_store.id
        print("Vector store created!")

        assistant = client.beta.assistants.create(
            instructions=assistant_instructions,
            model="gpt-4o",
            tools=[{
                "type": "file_search"
            }],
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store_id]
                }
            })

        with open(assistant_file_path, 'w') as file:
            IDs = {
                'assistant_id': assistant.id,
                'vector_store_id': vector_store_id
            }
            json.dump(IDs, file)

        assistant_id = assistant.id

    return assistant_id, vector_store_id
