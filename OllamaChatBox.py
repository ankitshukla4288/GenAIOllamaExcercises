#imports
import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown,display
from dotenv import load_dotenv
from openai import OpenAI

from Website import Website

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
message = "Hello Llama this is my first ever message to you Hi!"
response = openai.chat.completions.create(model='llama3.2', messages=[{"role":"user", "content": message}])
#print(response.choices[0].message.content)
ed = Website("https://aajtak.in")
#print(ed.title)
#print(ed.text)
system_prompt = "you are an assistant that analyzes the contents of a website\
& provides a short summary, ignoring the text that might be navigation related.\
Respond in markdown"
#print(system_prompt)

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\n The content of this website is as follows; \
    please provide a short summary of this website in markdown. \
    If it includes news or announcements, summarize that too \n \n"
    user_prompt += f"{website.text}"
    return user_prompt

#print(user_prompt_for(ed))

def messages_for(website):
    return [
        {"role":"system", "content":system_prompt},
        {"role":"user", "content":user_prompt_for(website)}
    ]

def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(model = "llama3.2", messages=messages_for(website))
    return response.choices[0].message.content

print(summarize("https://aajtak.in"))
def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))

#display_summary("https://edwarddonner.com")


