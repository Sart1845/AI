import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"
role="user"

# for structuring the output we can use pydantic model
from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str
    
schema=Ticket.model_json_schema()
Response_format={
    "type":"json_object"
}
system_prompt=f"""
extract the personal information from the ticket strictly based on  this schema.and give me json output.
{schema}
"""
message_system={
    "role": "system",
    "content": system_prompt
}
text="my name is pratyush . i have an iphone which is not working at all . my adresss is delhi. my email is abc@gmail.com .my contact is 81255"
prompt=f"""
This is the customer ticket.please extract the personal information from this.
{text} 
"""
# message me role and content
message={
    "role": "user",
    "content": prompt
}

messages=[message_system,message]

response=client.chat.completions.create(model=model, messages=messages,response_format=Response_format)

answer=response.choices[0].message.content
print(answer) 

# isko padhte kaise hai
import json
raw_json=answer
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)


# inko pass kr sakte hai aage!
print(ticket.name)
print(ticket.email)
print(ticket.issue)



#Homework

# take resume in pdf or word
# have hr give you a list of things like skill, experience, projects
# extract these from resume 
# match against the hr list
# generate a percentage of matching or not