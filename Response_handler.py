import re

class Response_handler:
    #Example: Start (1,3), next move (1,4), next move (4,3), next move (4,4), End (2,3)
    def clean_basic(response):
        # Define a regular expression pattern to match coordinates
        pattern = re.compile(r'\((\d+),(\d+)\)')

        # extract all matches
        matches = pattern.findall(str(response))

        # Convert the matches to tuples and store in a list
        coordinates = [(int(x),int(y)) for x, y in matches]
        return coordinates