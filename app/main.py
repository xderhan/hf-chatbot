from openai import OpenAI
import streamlit as st

# Avatars
user_avatar = "https://img.icons8.com/color/48/000000/user-male-circle--v1.png"
ai_avatar = "https://img.icons8.com/color/48/000000/bot.png"

def main():
    # Set the page title and icon
    st.set_page_config(page_title="HF Chatbot", page_icon="🤖", layout="centered")

    # Replicate Credentials
    with st.sidebar:
        st.title('Hugging Face Chatbot')
        st.write('This chatbot is created using LLM models from Hugging Face.')
        if 'HF_API_KEY' in st.secrets and st.secrets['HF_API_KEY'] != "":
            st.success('API key already provided!', icon='✅')
            hf_api_key = st.secrets['HF_API_KEY']
        else:
            hf_api_key = st.text_input('Enter Hugging Face API token:', type='password')
            if not (hf_api_key.startswith('hf_') and len(hf_api_key)==40):
                st.warning('Please enter your credentials!', icon='⚠️')
            else:
                st.success('Proceed to entering your prompt message!', icon='👉')

        st.subheader('Models and parameters')

        models = ["Qwen/Qwen2.5-72B-Instruct", "Qwen/Qwen2.5-Coder-32B-Instruct", "meta-llama/Llama-3.2-3B-Instruct"]
        st.sidebar.selectbox("Choose a model", models, key="selected_model")

        st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key="temperature")
        st.sidebar.slider("Max tokens", min_value=256, max_value=4096, value=2048, step=256, key="max_tokens")
        st.sidebar.slider("Top P", min_value=0.0, max_value=1.0, value=0.7, step=0.1, key="top_p")


    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "avatar": ai_avatar, "content": "How may I assist you today?"}]

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(name=message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "avatar": ai_avatar, "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    if "selected_model" not in st.session_state:
        st.session_state["selected_model"] = "Qwen/Qwen2.5-72B-Instruct"

    client = OpenAI(
        base_url="https://api-inference.huggingface.co/v1/",
        api_key=hf_api_key
    )

    # User-provided prompt
    if prompt := st.chat_input(disabled=not hf_api_key):
        st.session_state.messages.append({"role": "user", "avatar": user_avatar, "content": prompt})
        with st.chat_message("user", avatar=user_avatar):
            st.markdown(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar=ai_avatar):
            stream = client.chat.completions.create(
                model=st.session_state["selected_model"],
                messages=[
                    {"role": m["role"], "avatar": ai_avatar, "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=st.session_state["temperature"],
                max_tokens=st.session_state["max_tokens"], 
                top_p=st.session_state["top_p"],
                stream=True
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "avatar": ai_avatar, "content": response})

if __name__ == "__main__":
    main()