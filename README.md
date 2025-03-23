# 📞 Call Quality Analyzer

## 📝 Overview

The **Call Quality Analyzer** processes YAML conversation files to detect:

1. **Profanity & Compliance Violations** (Regex-based and LLM-based detection).
2. **Privacy Violations** (Sensitive information disclosure before identity verification).
3. **Call Metrics** (Overtalk & Silence percentages with visualizations).

## 🚀 Features

✅ **Regex-based Profanity Detection**  
✅ **LLM-based (Gemini) Profanity & Compliance Detection**  
✅ **Real-time Visualization for Call Metrics**  
✅ **Streamlit App for Easy Interaction**

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ParthNBarai/Prodigal.git
cd call-quality-analyzer
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_api_key_here
```

Or, export it manually:

```bash
export GEMINI_API_KEY=your_api_key_here
```

### 4️⃣ Run the Streamlit App

```bash
streamlit run app.py
```

## 📊 Visualization

The application provides:

- **Silence & Overtalk Analysis** through interactive graphs.
- **Detailed JSON reports** for flagged violations.

## 📝 Technical Details

- **Regex-based approach** is **fast** but limited to predefined lists.
- **LLM-based approach** (Gemini API) is **context-aware** but requires API calls.

## 🤝 Contributing

Feel free to raise issues or create pull requests! 🚀
