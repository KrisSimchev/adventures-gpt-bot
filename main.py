import openai
import functions
import time

OPENAI_API_KEY="openai-key"

client = openai.OpenAI(api_key=OPENAI_API_KEY)

assistant_id, vector_store_id = functions.create_assistant(
    client)

print("Starting a new conversation...")
thread = client.beta.threads.create(
    messages=[{
        "role": "user",
        "content": "Starting a new conversation."
    }],
    tool_resources={"file_search": {
        "vector_store_ids": [vector_store_id]
    }})
print(f"New thread created with ID: {thread.id}")


def chat(user_input, thread_id = thread.id):
  client.beta.threads.messages.create(thread_id=thread_id,
                                      role="user",
                                      content=user_input)
  
  run = client.beta.threads.runs.create(thread_id=thread_id,
                                        assistant_id=assistant_id)
  
  while True:
    run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                   run_id=run.id)
    print(f"Run status: {run_status.status}")
    if run_status.status == 'completed':
      break
    
    elif run_status.status == 'failed':
      error_response = {
          'error': 'Run status failed',
      }
      return error_response, 400
      
    time.sleep(1)

  messages = client.beta.threads.messages.list(thread_id=thread_id)
  response = messages.data[0].content[0].text.value

  return (response)

while True:
  user_input = input()
  start_time = time.time()
  response = chat(user_input=user_input)
  end_time = time.time()

  time_taken = end_time - start_time
  print(f"Response: {response}")
  print(f"Time taken: {time_taken:.2f} seconds")