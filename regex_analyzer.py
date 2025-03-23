import re
from profanity_list import PROFANE_WORDS

# Compile regex pattern once for efficiency
PROFANITY_REGEX = re.compile(r"\b(" + "|".join(map(re.escape, PROFANE_WORDS)) + r")\b", re.IGNORECASE)

def contains_profanity(text):
    """Returns a list of profane words found in the given text."""
    return re.findall(PROFANITY_REGEX, text)

def detect_profanity(yaml_data):
    """Detects profanity, returns count & list of detected profane words for each speaker."""
    profanity_results = {"Agent": {"count": 0, "words": []}, "Customer": {"count": 0, "words": []}}

    for entry in yaml_data:
        speaker = entry["speaker"]
        text = entry["text"]

        profane_words = contains_profanity(text)  # Get profane words in text
        profanity_results[speaker]["count"] += len(profane_words)
        profanity_results[speaker]["words"].extend(profane_words)  # Store detected words

    return profanity_results


# Privacy & Compliance Detection
SENSITIVE_INFO = ["balance", "account number", "amount due"]
VERIFICATION_QUESTIONS = ["date of birth", "address", "SSN", "social security number"]

def detect_compliance_violations(yaml_data):
    """Detects privacy and compliance violations in conversations."""
    verification_done = False
    violation_flag = False
    flagged_statements = []

    for entry in yaml_data:
        if entry["speaker"] == "Agent":
            text = entry["text"].lower()

            # Check for verification
            if any(phrase in text for phrase in VERIFICATION_QUESTIONS):
                verification_done = True

            # Check for sensitive information disclosure
            elif any(phrase in text for phrase in SENSITIVE_INFO):
                if not verification_done:
                    violation_flag = True
                    flagged_statements.append(f"❌ {entry['speaker']}: {entry['text']}")  # Store flagged statements

    return violation_flag, flagged_statements
