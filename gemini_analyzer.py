import google.generativeai as genai
import os

# Set up Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Use environment variable for security
genai.configure(api_key=GEMINI_API_KEY)

# Function to analyze text using Gemini API
def analyze_with_gemini(yaml_data, analysis_type):
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Prepare conversation text
    conversation_text = "\n".join([f"{entry['speaker']}: {entry['text']}" for entry in yaml_data])

    if analysis_type == "Profanity Detection":
        prompt = f"""
        Analyze the following conversation and detect any profanity used.
        Return a JSON output with the flagged speaker and words.

        Conversation:
        {conversation_text}
        """
    
    elif analysis_type == "Privacy and Compliance Violation":
        prompt = f"""
        Analyze the following conversation and detect any privacy or compliance violations.
        Specifically, flag instances where sensitive information is disclosed **without proper user verification**.
        Return a JSON output with flagged statements.

        Conversation:
        {conversation_text}
        """

    response = model.generate_content(prompt)
    return response.text if response else "No response from Gemini API."
