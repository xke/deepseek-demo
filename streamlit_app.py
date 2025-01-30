import streamlit as st
from groq import Groq

st.set_page_config(page_title="Deepseek Demo", page_icon="💬", layout="wide")

# Show title and description.
st.title("💬 Deepseek Demo Chatbot")
st.write(
    "Can open-source AI models solve your problems? 🤔 "
)

#from huggingface_hub import InferenceClient
# got error from below: unexpected keyword argument 'provider'
# client = InferenceClient(
#	provider="together",
#	api_key=st.secrets["HF_TOKEN"]
# )

#from openai import OpenAI
# below ran into quota issue:
#client = OpenAI(
#	base_url="https://huggingface.co/api/inference-proxy/together",
#	api_key=st.secrets["HF_TOKEN"]
#)

st.sidebar.title('Customization')
model = st.sidebar.selectbox(
    'Choose an open-source model',
    ['deepseek-r1-distill-llama-70b', 'llama-3.3-70b-versatile', 'mixtral-8x7b-32768', 'gemma2-9b-it']
)


st.sidebar.write("")
st.sidebar.write("")
st.sidebar.markdown(
"""
This is an open-source demo app by [@xke](https://github.com/xke/deepseek-demo).
""",
    unsafe_allow_html=True
)

client = Groq(
        api_key = st.secrets["GROQ_API_KEY"], 
)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Ask the chatbot anything! Type here..."):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Function to handle streaming response
    def stream_response():
        # Generate a response
        chat_completion = client.chat.completions.create(
            model=model, 
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        for chunk in chat_completion:
            # Ensure chunk has choices and extract content
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream_response)
    st.session_state.messages.append({"role": "assistant", "content": response})
