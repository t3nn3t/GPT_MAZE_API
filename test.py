
from openai import OpenAI




client = OpenAI()

instruction = "You are a helpful assistant"
prompt = "What is your maximum length of output"


def ask_gpt(prompt):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": instruction},
    {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message.content

print(ask_gpt(prompt))
