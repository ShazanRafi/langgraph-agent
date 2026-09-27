from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core import prompts, messages
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage,BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from typing import TypedDict, Annotated

load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    max_new_tokens=256,
    temperature=0.7,
)

model=ChatHuggingFace(llm=llm)

class ChatState(TypedDict):
    message: Annotated[list[BaseMessage], add_messages]

def chatnode(state: ChatState):

    message = state['message']
    response = model.invoke(message)

    return {'message': [response]}

checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

graph.add_node('chatnode', chatnode)

graph.add_edge(START, 'chatnode')
graph.add_edge('chatnode', END)

chatbot = graph.compile(checkpointer=checkpointer)

thread_id = 1
while True:

    user_input = input('write here: ')

    if user_input.strip().lower() in ['exit', 'quit', 'bye']:
        break

    config = {'configurable': {'thread_id': thread_id}}
    response = chatbot.invoke({'message': HumanMessage(user_input)}, config=config)
    AIresponse = response['message'][-1].content
    print("AI: ", AIresponse) 
