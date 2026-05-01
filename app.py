import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

load_dotenv()

def highlight_code(code: str) -> str:
    return highlight(code, PythonLexer(), HtmlFormatter(style="monokai", linenos=True))

st.set_page_config(page_title="Roast My Code 🔥", page_icon="💀", layout="wide")
st.title("💀 AI Roast My Code")
st.markdown("### Because your code needs savage feedback")

col1, col2 = st.columns([3, 1])

with col1:
    code_input = st.text_area("Paste your Python code here", height=500, placeholder="def bad_function()...")

with col2:
    roast_level = st.selectbox("Roast Level", ["gentle", "spicy", "nuclear"], index=1)
    api_key = st.text_input("Groq API Key (optional)", type="password", value=os.getenv("GROQ_API_KEY", ""))
    
    if st.button("ROAST THIS CODE 🔥", type="primary", use_container_width=True):
        if not code_input.strip():
            st.error("You forgot to paste code 💀")
        else:
            with st.spinner("Summoning the roast gods..."):
                try:
                    client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are a brutally honest and hilarious senior Python engineer. Roast the code with savage humor but also give real improvements."},
                            {"role": "user", "content": f"Roast level: {roast_level.upper()}\n\nCode:\n{code_input}"}
                        ],
                        temperature=0.85,
                        max_tokens=1500,
                        stream=True
                    )
                    
                    roast_text = ""
                    roast_container = st.empty()
                    for chunk in response:
                        if chunk.choices[0].delta.content:
                            roast_text += chunk.choices[0].delta.content
                            roast_container.markdown(roast_text)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    
st.caption("Made with ❤️ and zero mercy")
