import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Load API Key ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY not found. Please set it in your .env file or Streamlit secrets.")
    st.stop()

# --- Configure Gemini ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# --- System Prompt ---
SYSTEM_PROMPT = """
You are an expert AI Research Assistant. 
The user will provide a research topic or question.

Your task:
1️⃣ Research and synthesize knowledge *from your trained data* (no browsing).  
2️⃣ Provide a clear, concise, and structured explanation using Markdown format.  

Format the output as follows:

**🔑 Key Concepts:**  
Summarize the most important technical ideas concisely.

**🧩 Step-by-Step Explanation:**  
Explain how the concept works or can be built.

**💡 Practical Use Cases:**  
Give 2–3 real-world examples or applications.

**🚀 Implementation Hints:**  
Provide short, practical tips or pseudocode for implementation.
"""

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="AI Research Assistant")
st.title("🤖 AI Research Assistant")

# --- Input ---
user_query = st.text_input("Enter your research topic:", placeholder="e.g., How to build a RAG system with LLMs")

if st.button("Start Research"):
    if not user_query:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("🧠 Researching and summarizing using Gemini..."):
            try:
                full_prompt = f"{SYSTEM_PROMPT}\n\n--- USER QUERY ---\n{user_query}\n\n"
                response = model.generate_content(full_prompt)
                st.success("✅ Research Completed!")
                st.balloons()
                st.markdown(response.text)

            except Exception as e:
                st.error(f"⚠️ Error: {e}")
                st.info("Please check your API key or try again later.")
