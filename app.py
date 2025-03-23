import streamlit as st
import yaml
from regex_analyzer import detect_profanity, detect_compliance_violations  # Import detection functions
from gemini_analyzer import analyze_with_gemini  # Import Gemini detection function

# Function to load YAML file
def load_yaml(file):
    return yaml.safe_load(file)

# Streamlit UI
st.title("Conversation Analysis Tool")

# File upload
uploaded_file = st.file_uploader("Upload a YAML file", type=["yaml", "yml"])

# Dropdown for entity type
entity_type = st.selectbox("Select Entity to Analyze", ["Profanity Detection", "Privacy and Compliance Violation"])

# Dropdown for detection approach
approach = st.selectbox("Select Detection Approach", ["Regex", "Gemini AI"])

if uploaded_file:
    yaml_data = load_yaml(uploaded_file)

    if approach == "Regex":
        if entity_type == "Profanity Detection":
            profanity_results = detect_profanity(yaml_data)
            st.subheader("Profanity Detection (Regex)")

            st.write("### 🔹 Profanity Counts & Words")
            st.write(f"👤 **Agent:** {profanity_results['Agent']['count']} profane words detected - {profanity_results['Agent']['words']}")
            st.write(f"👤 **Customer:** {profanity_results['Customer']['count']} profane words detected - {profanity_results['Customer']['words']}")

        elif entity_type == "Privacy and Compliance Violation":
            violation_flag, flagged_statements = detect_compliance_violations(yaml_data)
            st.subheader("Privacy & Compliance Violation (Regex)")

            if violation_flag:
                st.write("🚨 **Violations detected!**")
                st.write(flagged_statements)
            else:
                st.write("✅ No violations found.")

    elif approach == "Gemini AI":
        st.subheader(f"{entity_type} (Gemini AI)")
        
        gemini_response = analyze_with_gemini(yaml_data, entity_type)
        st.write(gemini_response)
