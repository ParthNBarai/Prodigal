import streamlit as st
import yaml
import matplotlib.pyplot as plt
from analyzers.regex_analyzer import detect_profanity, detect_compliance_violations  
from analyzers.gemini_analyzer import analyze_with_gemini  
from call_quality.call_quality_analyzer import calculate_call_metrics  

# Function to load and parse YAML file
def load_yaml(file):
    return yaml.safe_load(file)

# Streamlit UI setup
st.title("Conversation Analysis Tool")

# File upload section
uploaded_file = st.file_uploader("Upload a YAML file", type=["yaml", "yml"])

# Dropdown for selecting the type of analysis
entity_type = st.selectbox("Select Entity to Analyze", [
    "Profanity Detection", "Privacy and Compliance Violation"
])

# Dropdown for selecting the detection approach (only for Profanity & Compliance)
approach = st.selectbox("Select Detection Approach", ["Regex", "Gemini AI"]) if entity_type else None

# Proceed if a file is uploaded
if uploaded_file:
    yaml_data = load_yaml(uploaded_file)

    # Profanity Detection
    if entity_type == "Profanity Detection":
        if approach == "Regex":
            # Perform profanity detection using Regex
            profanity_results = detect_profanity(yaml_data)
            st.subheader("Profanity Detection (Regex)")
            st.write("### 🔹 Profanity Counts & Words")
            st.write(f"👤 **Agent:** {profanity_results['Agent']['count']} profane words detected - {profanity_results['Agent']['words']}")
            st.write(f"👤 **Customer:** {profanity_results['Customer']['count']} profane words detected - {profanity_results['Customer']['words']}")

        elif approach == "Gemini AI":
            # Perform profanity detection using Gemini AI
            st.subheader("Profanity Detection (Gemini AI)")
            gemini_response = analyze_with_gemini(yaml_data, "Profanity Detection")
            st.write(gemini_response)

    # Privacy & Compliance Violation Detection
    elif entity_type == "Privacy and Compliance Violation":
        if approach == "Regex":
            # Detect compliance violations using Regex
            violation_flag, flagged_statements = detect_compliance_violations(yaml_data)
            st.subheader("Privacy & Compliance Violation (Regex)")
            if violation_flag:
                st.write("🚨 **Violations detected!**")
                st.write(flagged_statements)
            else:
                st.write("✅ No violations found.")

        elif approach == "Gemini AI":
            # Detect compliance violations using Gemini AI
            st.subheader("Privacy & Compliance Violation (Gemini AI)")
            gemini_response = analyze_with_gemini(yaml_data, "Privacy and Compliance Violation")
            st.write(gemini_response)
    
    # Call Quality Analysis (Always Runs)
    st.subheader("📞 Call Quality Metrics")
    silence_percentage, overtalk_percentage = calculate_call_metrics(yaml_data)

    # Display calculated metrics
    st.write(f"🔇 **Silence Percentage:** {silence_percentage:.2f}%")
    st.write(f"🗣️ **Overtalk Percentage:** {overtalk_percentage:.2f}%")

    # Visualization for call quality metrics
    fig, ax = plt.subplots()
    ax.bar(["Silence", "Overtalk"], [silence_percentage, overtalk_percentage], color=["blue", "red"])
    ax.set_ylabel("Percentage (%)")
    ax.set_title("Call Quality Metrics")
    st.pyplot(fig)
