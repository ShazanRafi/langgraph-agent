import streamlit as st
from chatbot import chatbot, retrieve_all_thread
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage,BaseMessage
import uuid

#utility functions
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def add_threads(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_threads(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def load_conversation(thread_id):
    config = {'configurable': {'thread_id': thread_id}}
    messages = chatbot.get_state(config=config).values['messages']
    temp_message = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            role = 'user'
        else:
            role = 'assistant'
        temp_message.append({'role': role, 'content': msg.content})
    return temp_message


#session_state
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_thread()

add_threads(st.session_state['thread_id'])

#sidebar
st.sidebar.title('NexaBot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        st.session_state['message_history'] = load_conversation(thread_id)
        

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('type here')

if user_input:

    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    config = {
            'configurable': {'thread_id': st.session_state['thread_id']},
            'metadata': {'thread_id': st.session_state['thread_id']},
            'run_name': 'chat_turn'}

    with st.chat_message('assistant'):
        ai_response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'message': HumanMessage(user_input)},
                config=config,
                stream_mode= 'messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_response})