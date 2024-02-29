import re
import time
from openai import OpenAI
import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.auth import default
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials

class Response_handler:

    def __init__(self, model, prompt):

        self.client = OpenAI()
        self.model = model

        f = open(prompt, "r")
        p = open("user_prompt_v1.0", "r")
        d = open("default_sys_prompt.txt", "r")

        self.instruction = f.read()
        self.prompt = p.read()
        self.default_sys = d.read()


    def ask_gpt(self, post_prompt):
        full_prompt = (self.instruction + "\n\n" +self.prompt + post_prompt)
        print("\nAsking ChatGPT:\n"+full_prompt+"\n")
        completion = self.client.chat.completions.create(
        model=self.model,
        messages=[
        {"role": "system", "content": self.default_sys},
        {"role": "user", "content": (full_prompt)}
        ],
        max_tokens=2000,
        temperature=1
        )
        return completion.choices[0].message.content
    

    def ask_gemini(self, post_prompt: str) -> str:
        full_prompt = (self.instruction + "\n\n" +self.prompt + post_prompt)
        print("\nAsking Gemini:\n"+(full_prompt)+"\n")
        vertexai.init(project="clear-ranger-415717", location="europe-west2")
        model = GenerativeModel("gemini-1.0-pro")
        # Load the model
        #model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(full_prompt)

        #sleep to not reach api response limit
        time.sleep(4)
        return response.text



    #Example: Start (1,3), next move (1,4), next move (4,3), next move (4,4), End (2,3)
    def clean_basic(self, response):
        # Define a regular expression pattern to match coordinates
        pattern = re.compile(r'\((\d+),(\d+)\)')

        # extract all matches
        matches = pattern.findall(str(response))

        # Convert the matches to tuples and store in a list
        coordinates = [(int(x),int(y)) for x, y in matches]
        if (len(coordinates)==0):
            pattern = re.compile(r'\((\d+),\s*(\d+)\)')

            # extract all matches
            matches = pattern.findall(str(response))

            # Convert the matches to tuples and store in a list
            coordinates = [(int(x),int(y)) for x, y in matches]
        print('\ncleaned:')
        print(coordinates)
        print("")
        return coordinates
    

    #Example: move list: (1,3) -> (1,4), (4,3)->(4,4) end of move list
    #         Start (1,3), next move (1,4), next move (4,3), next move (4,4), End (2,3)
    def clean_adv(self, response):
        # Define a regular expression pattern to match coordinates
        pattern = r'Start(.*)'
        move_chain = re.search(pattern, response)

        if move_chain is None:
            print("NO MOVES FROM LLM")
            return self.clean_basic("(-1,-1)")
        move_chain = move_chain.group()

        return self.clean_basic(move_chain)
    

    #Example: Start (1,3), connection "(1,3) <--> (1,4)" next move (1,4), connection "(1,4) <--> (2,3)" End (2,3)
    def clean_cot(self, response):
        # Define a regular expression pattern to match coordinates
        pattern = r'(?<!")\((\d+,\d+)\)(?!")'
        move_chain = re.findall(pattern, response)
        move_chain = "("+('), ('.join(move_chain))+")"
        
        if move_chain is None:
            return self.clean_basic("(-1,-1)")
        
        move_chain = "Start "+move_chain

        return self.clean_basic(move_chain)
    

#Example: Start "(1,3)", connection (1,3) <--> (1,4) next move "(1,4)", connection (1,4) <--> (2,3) End "(2,3)"
    def clean_quoted(self, response):
        print("cleaning quoted: ")
        print(response)
        # Define a regular expression pattern to match coordinates
        pattern = r'"\((\d+,\d+)\)"'
        move_chain = re.findall(pattern, response)
        move_chain = "("+('), ('.join(move_chain))+")"
        
        if move_chain is None:
            return self.clean_basic("(-1,-1)")
        
        move_chain = "Start "+move_chain

        return self.clean_basic(move_chain)