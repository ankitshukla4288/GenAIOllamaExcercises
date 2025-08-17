import requests

class OllamaChatClient:

    def __init__(self, apiUrl="http://localhost:11434/api/chat", model = "llama3.2"):
        self.header = {"Content-Type": "application/json"}
        self.model = model
        self.apiUrl = apiUrl

    def __chat__(self, prompt, stream = False):
        #send a prompt to Ollama & get back response
        messages = [{"role":"user", "content": prompt}]
        payload = {"model" : self.model,"messages" : messages,  "stream": stream }
        response = requests.post(url=self.apiUrl, json=payload, headers=self.header)
        if stream:
           #streamed response come line by line
           for line in response.iter_lines():
               if line:
                   data = line.decode("utf-8")
                   print(data, flush=True)
           return None
        else:
            return response.json()["message"]["content"]

#Example Usage
if __name__ == "__main__":
    client = OllamaChatClient()
    answer = client.__chat__("Describe Generative AI")
    print ("Ollama response", answer)