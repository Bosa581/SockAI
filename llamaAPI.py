#using llama to access its apis for user interactions
import json
import requests
class llamaAPI:
    def __init__(self, model="llama3"): # default constructor
        self.model = model
        self.user_prev_prompt = None
        self.ai_prev_response = None
        #second construtor that will take the user's previous message. This will be used to create the memory for the model
    def getPrevMessage(self,user_prev_prompt,ai_prev_response):
        self.ai_prev_response = ai_prev_response
        self.user_prev_prompt = user_prev_prompt
 
    def get_response(self,prompt):
        url = "http://localhost:11434/api/chat" #api call
        #payload- internal structure is that of a dictionary
        if not self.ai_prev_response or not self.user_prev_prompt:
            payload = { # for the first prompt
            "model": self.model,
            "messages": [{"role": "user", "content": prompt }],
            "stream": False
            }
        else:
            payload = {  # accomodates multiple conversations, in hoopes that it resolves the issue of not printing the ai's response when there isnt a previous response
                "model": self.model,
                "messages": [{"role": "user","content": self.user_prev_prompt},
                            {"role": "assistant", "content": self.ai_prev_response},
                            {"role":"user", "content":prompt}],
                "stream": False #only sends message after response is fully generated
            }
        try:
            response = requests.post(url,json = payload)
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"[Request failed] {e}"
        except (KeyError, TypeError):
            return "[Unexpected response format]"