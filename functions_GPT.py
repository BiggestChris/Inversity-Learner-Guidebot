# Script to host ChatGPT functions - taken from other Inversity projects

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def comprehend_data(input_data):

    completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                 {"role": "system", 
                  "content": """This is meant to be a guide for people learning to code on their GitHub. Can you please read the file
                  that you will be given and write a paragraph on general feedback for the user.
                  """},
                {"role": "user",
                 "content": input_data }
            ]
        )

    output = completion.choices[0].message.content

    # print(output)

    return output