import pathlib
import textwrap

import google.generativeai as genai

# Used to securely store your API Key
# from google.colab import userdata

from IPython.display import display
from IPython.display import Markdown

import os 
os.environ['GOOGLE_API_KEY'] = "AIzaSyDDw4i32pQfN9gRlRAI5JFEg-hzjzlIpLI"

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def modify_msg(message):
    # Add your code here to modify the message as per requirement.
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(message + "Give answer in 50 to 100 words.")
    response2 = model.generate_content("Give me a top 10 links related to " + message)
    return response.text, response2.text