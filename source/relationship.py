import openai
import time
from apikey import apikey
openai.api_key = apikey

def AI(prompt:str,engine ="gpt-3.5-turbo-1106"):
    completion = openai.ChatCompletion.create(
    model = engine,
    messages = [{'role': 'user', 'content': prompt}],
    max_tokens=1200,
    temperature = 0.2)
    response=completion['choices'][0]['message']['content']
    return response
print(AI("What is the meaning of life?"))