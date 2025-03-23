from analyzers.regex_analyzer import detect_profanity

# Sample conversation data
sample_yaml = [
    {"speaker": "Agent", "text": "Hello, how are you?"},
    {"speaker": "Customer", "text": "What the hell do you want? I'm busy!"},
    {"speaker": "Agent", "text": "I understand. Can we discuss your account?"},
    {"speaker": "Customer", "text": "You can shove it! I'm not paying!"},
]

# Run detection
result = detect_profanity(sample_yaml)

# Print results
print("Flagged Calls:")
print("Agent:", result["Agent"])
print("Customer:", result["Customer"])
