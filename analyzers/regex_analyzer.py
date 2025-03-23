import re
from analyzers.profanity_list import PROFANE_WORDS

# Compile regex pattern once for efficiency
PROFANITY_REGEX = re.compile(r"\b(" + "|".join(map(re.escape, PROFANE_WORDS)) + r")\b", re.IGNORECASE)

# Keywords related to sensitive financial data
SENSITIVE_INFO = ["balance", "account number", "amount due", "outstanding balance"]

# Common verification questions asked by agents
VERIFICATION_QUESTIONS = ["date of birth", "address", "SSN", "social security number", "verify your identity"]

def contains_profanity(text):
    """Returns a list of profane words found in the given text."""
    return re.findall(PROFANITY_REGEX, text)

def detect_profanity(yaml_data):
    """Detects profanity in conversations and returns counts and detected words."""
    profanity_results = {"Agent": {"count": 0, "words": []}, "Customer": {"count": 0, "words": []}}

    for entry in yaml_data:
        speaker = entry["speaker"]
        text = entry["text"]

        profane_words = contains_profanity(text)  # Check for profane words in text
        profanity_results[speaker]["count"] += len(profane_words)
        profanity_results[speaker]["words"].extend(profane_words)  # Store detected words

    return profanity_results

# Privacy & Compliance Detection
def detect_compliance_violations(yaml_data):
    """Checks if an agent shares sensitive information without verifying customer identity."""
    verification_done = False  # Tracks whether verification was completed

    for i in range(len(yaml_data)):
        entry = yaml_data[i]
        text = entry["text"].lower()

        # Step 1: Agent asks a verification question
        if entry["speaker"] == "Agent" and any(phrase in text for phrase in VERIFICATION_QUESTIONS):
            verification_done = False  # Reset verification status
            continue  

        # Step 2: Customer provides a response (likely containing digits)
        if entry["speaker"] == "Customer" and any(char.isdigit() for char in text):
            verification_done = True  # Mark verification as complete
            continue  

        # Step 3: Customer denies verification or refuses to provide info
        if entry["speaker"] == "Customer" and any(word in text for word in ["no", "not", "screw", "refuse", "won't", "hell no"]):
            verification_done = False  # Reset verification status
            continue  

        # Step 4: Agent shares sensitive information without completed verification
        if entry["speaker"] == "Agent" and any(phrase in text for phrase in SENSITIVE_INFO):
            if not verification_done:
                return True, f"❌ Privacy Violation: {entry['speaker']} disclosed sensitive info **without completed verification**: \"{entry['text']}\""

    return False, None  # No violations detected
