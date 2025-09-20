import pathlib
import textwrap

# Used to securely store your API Key
# from google.colab import userdata
import os 

def modify_msg(message):
    # Add your code here to modify the message as per requirement.
    # Lazy import to avoid breaking Django startup if dependency is missing
    try:
        import google.generativeai as genai
    except Exception:
        # Gracefully degrade if package is not installed
        return (
            "AI service is not available because 'google-generativeai' is not installed.",
            ""
        )

    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        return (
            "AI service is not configured. Please set the GOOGLE_API_KEY environment variable.",
            ""
        )

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(message + " Give answer in 50 to 100 words.")
        response2 = model.generate_content("Give me a top 10 links related to " + message)
        return response.text, response2.text
    except Exception as e:
        # Return a friendly message if the API call fails for any reason
        return (f"AI service error: {e}", "")