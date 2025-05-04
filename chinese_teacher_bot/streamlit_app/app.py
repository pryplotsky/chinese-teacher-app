import streamlit as st
import requests

# Ollama API endpoint (default if running locally)
OLLAMA_API_URL = ""

# Streamlit page settings
st.set_page_config(page_title="AI-Powered Chinese Teacher", layout="centered")

st.title("🧑‍🏫 AI-Powered Chinese Teacher")
st.subheader("Practice Mandarin Chinese with AI (Powered by TinyLlama)")

# Initialize conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are a helpful, patient Mandarin Chinese teacher. "
            "Correct grammar, suggest better phrasing, and explain corrections in English. "
            "Encourage the student when they do well!"
        )}
    ]

# Function to send messages to Ollama running TinyLlama
def chat_with_tinyllama():
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "tinyllama",  # <- Swapped from 'mistral' to 'tinyllama'
        "messages": st.session_state.messages,  # Send entire conversation history
        # TinyLlama might not support "stream", so we leave it out or set False
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Debug output (optional): print(result)

        # Extract content depending on Ollama version
        return result["message"]["content"] if "message" in result else result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"

# User input box
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your sentence in Mandarin Chinese:")
    submitted = st.form_submit_button("Send")

# Handle user message submission
if submitted and user_input:
    # Add user's message to the conversation history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get AI response
    with st.spinner("Thinking..."):
        ai_response = chat_with_tinyllama()

    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Display chat history (exclude the system message)
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"👤 **You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"🤖 **AI Teacher:** {message['content']}")

# Clear conversation button
if st.button("Reset Chat"):
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are a helpful, patient Mandarin Chinese teacher. "
            "Correct grammar, suggest better phrasing, and explain corrections in English. "
            "Encourage the student when they do well!"
        )}
    ]
