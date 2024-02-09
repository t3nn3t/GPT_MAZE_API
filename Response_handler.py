import re
from openai import OpenAI

class Response_handler:

    def __init__(self):

        self.client = OpenAI()
        f = open("system_prompt_v1.1", "r")
        p = open("user_prompt_v1.0", "r")
        self.instruction = f.read()
        self.prompt = p.read()


    def ask_gpt(self, post_prompt):
        print("Asking ChatGPT: "+(self.prompt + post_prompt))
        completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": self.instruction},
        {"role": "user", "content": (self.prompt + post_prompt)}
        ]
        )
        return completion.choices[0].message.content



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
        return coordinates
    

    #Example: move list: (1,3) -> (1,4), (4,3)->(4,4) end of move list
    #         Start (1,3), next move (1,4), next move (4,3), next move (4,4), End (2,3)
    def clean_adv(self, response):
        print(response)
        # Define a regular expression pattern to match coordinates
        pattern = r'Start(.*)'
        move_chain = re.search(pattern, response)

        if move_chain is None:
            self.clean_basic("(-1,-1)")
        move_chain = move_chain.group()

        return self.clean_basic(move_chain)