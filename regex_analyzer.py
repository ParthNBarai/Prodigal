import re
from profanity_list import PROFANE_WORDS

# Compile regex pattern once for efficiency
PROFANITY_REGEX = re.compile(r"\b(" + "|".join(map(re.escape, PROFANE_WORDS)) + r")\b", re.IGNORECASE)

def contains_profanity(text):
    """Returns a list of profane words found in the given text."""
    matches = re.findall(PROFANITY_REGEX, text)
    return matches  

def detect_profanity(yaml_data):
    """Detects profanity, returns count & list of detected profane words for each speaker."""
    profanity_results = {"Agent": {"count": 0, "words": []}, "Customer": {"count": 0, "words": []}}

    for entry in yaml_data:
        speaker = entry["speaker"]
        text = entry["text"]

        profane_words = contains_profanity(text)  
        profanity_results[speaker]["count"] += len(profane_words)
        profanity_results[speaker]["words"].extend(profane_words)  # Store detected words

    return profanity_results

