import streamlit as st
import yaml
from regex_analyzer import detect_profanity  
from gemini_analyzer import analyze_with_gemini

def load_yaml(file):
    return yaml.safe_load(file)

# Streamlit UI
st.title("Profanity Detection in Conversations")

uploaded_file = st.file_uploader("Upload a YAML file", type=["yaml", "yml"])

approach = st.selectbox("Select Detection Approach", ["Regex", "Gemini AI"])

if uploaded_file:
    yaml_data = load_yaml(uploaded_file)

    if approach == "Regex":
        flagged_calls = detect_profanity(yaml_data)

        # Display results
        st.subheader("Profanity Detection (Regex)")
        st.write("### Agent Calls with Profanity")
        st.write(flagged_calls["Agent"] if flagged_calls["Agent"] else "No profanity detected")

        st.write("### Customer Calls with Profanity")
        st.write(flagged_calls["Customer"] if flagged_calls["Customer"] else "No profanity detected")

    elif approach == "Gemini AI":
        st.subheader("Profanity Detection (Gemini AI)")
        gemini_response = analyze_with_gemini(yaml_data)
        st.write(gemini_response)
