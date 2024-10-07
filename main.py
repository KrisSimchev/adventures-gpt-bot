<<<<<<< HEAD
import openai
import functions
import time
import re
from typing_extensions import override
from openai import AssistantEventHandler
from prompts import assistant_instructions

OPENAI_API_KEY="openai-api"

client = openai.OpenAI(api_key=OPENAI_API_KEY)

assistant_id, vector_store_id = functions.create_assistant(
    client)

class EventHandler(AssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.snapshot = {}
        self.start_time = time.time()

    @override
    def on_text_created(self, text):
        print("\n")
        #print("\nAssistant: ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
        self.snapshot = snapshot 
        if self.start_time is not None and '.' in delta.value or '!' in delta.value:
                    elapsed_time = time.time() - self.start_time
                    print(f"\nTime to first sentence: {elapsed_time:.2f} seconds\n")
                    self.start_time = None

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))



def chat():
    thread = client.beta.threads.create()
    while True:
        user_message = input("\nUser: ")
        start_time = time.time()

        message = client.beta.threads.messages.create(
          thread_id=thread.id,
          role="user",
          content=user_message
        )

        with client.beta.threads.runs.stream(
          thread_id=thread.id,
          assistant_id=assistant_id,
          instructions=assistant_instructions,
          event_handler=EventHandler(),
        ) as stream:
          stream.until_done()
chat()
