import streamlit as st
from app import chatbot
from langchain_core.messages import HumanMessage
def extract_text(message_chunk):
    content = message_chunk.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )

    return ""

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input('Type here')
if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    with st.chat_message('assistant'):

        # ai_message = st.write_stream(
        #     message_chunk.content for message_chunk, metadata in chatbot.stream(
        #         {'messages': [HumanMessage(content=user_input)]},
        #         config= {'configurable': {'thread_id': 'thread-1'}},
        #         stream_mode= 'messages'
        #     )
        # )
        ai_message = st.write_stream(
    extract_text(message_chunk)
    for message_chunk, metadata in chatbot.stream(
        {'messages': [HumanMessage(content=user_input)]},
        config=CONFIG,
        stream_mode='messages'
    )
)

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
