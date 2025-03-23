import google.generativeai as genai
import os

# Set up Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Fetch API key from environment variables
genai.configure(api_key=GEMINI_API_KEY)

# Function to analyze text using Gemini API
def analyze_with_gemini(yaml_data, analysis_type):
    """
    Uses the Gemini AI model to analyze conversation transcripts.
    
    Parameters:
        - yaml_data (list): A list of conversation entries, each containing 'speaker' and 'text'.
        - analysis_type (str): Type of analysis to perform ("Profanity Detection" or "Privacy and Compliance Violation").

    Returns:
        - str: The AI-generated response from Gemini.
    """

    # Initialize the AI model (using a lightweight variant for speed)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Convert YAML conversation data into a readable text format
    conversation_text = "\n".join([f"{entry['speaker']}: {entry['text']}" for entry in yaml_data])

    # --- Profanity Detection ---
    if analysis_type == "Profanity Detection":
        prompt = f"""
        Analyze the following conversation and detect any profanity used.
        Return a JSON output with the flagged speaker and words.

        **Conversation (Attached Below):**
        {conversation_text}
        """

    # --- Privacy & Compliance Violation Detection ---
    elif analysis_type == "Privacy and Compliance Violation":
        prompt = f"""
        ## Privacy and Compliance Violation Detection

        **Context:**
        You are analyzing a **real customer service call transcript** to detect **privacy and compliance violations**.  
        The conversation is **attached below**, and all responses **must be strictly based on this attached conversation**.

        **Task:**
        - Identify cases where an **agent shared sensitive financial information** (such as account balance, overdue amount, or account details) **without verifying the customer's identity**.
        - The verification should have happened **before** disclosing financial details.

        **Valid Identity Verification Includes:**
        - Asking for **Date of Birth (DOB)**
        - Asking for **Address**
        - Asking for **Social Security Number (SSN)**
        
        **Rules for Flagging Violations:**
        - If **none** of the above verifications were performed **before** financial disclosure → **Flag as a violation**.
        - If **verification was performed before disclosure** → **Do NOT flag it**.
        - **Do NOT create violations for statements that do not exist in the attached conversation.**  
        - If no violations exist in the conversation, return an **empty list `[]`**.

        **Expected Output Format:**
        - Return a **list of flagged statements** where a violation occurred.
        - For each flagged statement, provide:
          1. The **exact statement** where the agent disclosed financial details.
          2. The **preceding statements** to confirm whether verification was attempted.
          3. A **brief reason** why the statement was flagged as a violation.
          4. The **timestamp range (stime - etime)** for locating the violation.

        **Example Output:**
        ```json
        [
            {{
                "speaker": "Agent",
                "statement": "You have an overdue balance of $450.",
                "preceding_context": "No identity verification before this statement.",
                "reason": "Agent disclosed financial details without verifying DOB, Address, or SSN.",
                "timestamp": "27 - 34 seconds"
            }}
        ]
        ```

        **Important Instructions:**
        1. **Only use statements from the conversation attached below.**
        2. **Cross-check** before flagging to ensure accuracy.
        3. **Avoid false positives** and hallucinated responses.
        4. If no violations exist, return an **empty list `[]`**.
        
        **Conversation (Attached Below):**
        {conversation_text}
        """

    # Generate AI response based on the prompt
    response = model.generate_content(prompt)

    # Return the AI-generated analysis or a fallback message if there's no response
    return response.text if response else "No response from Gemini API."
