import streamlit as st

# message_history = []
if 'message_history' not in st.sessional_state:
    st.sessional_state['message_history'] = []

for message in st.sessional_state['message_history']:
    st.chat_message(message['role'])
    st.text(message['content'])

user_input = st.chat_input('type here')

if user_input:

    st.sessional_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    st.sessional_state['message_history'].append({'role': 'agent', 'content': 'response'})
    with st.chat_message('assistant'):
        st.text('response')