import os
from openai import OpenAI

client = OpenAI(
    api_key="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",
)

file = client.files.create(
  file=open("gpt.csv", "rb"),
  purpose='assistants'
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a League of Legends expert and watch every professional game of every league."},
    {"role": "user", "content": "I'll send you a database with professional matches and all the events that happened in each of them. The goal is for you to analyze what are the most impactful events in a match, what are the conditions for victory, and that in the future you try to predict an outcome based on some events that have already happened in a match."},    
  ],
  file_ids=[file.id],
)

print(completion.choices[0].message)