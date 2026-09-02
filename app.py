from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,AIMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]


def chat_node(state: ChatState):

    # take user query from state
    messages = state['messages']

    # send to llm
    response = llm.invoke(messages)
    clean_response = AIMessage(
        content=response.content[0]['text']
    )
    # response store state
    return {'messages': [clean_response]}

graph=StateGraph(ChatState)

graph.add_node("chat_node",chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)
checkpointer=InMemorySaver()
chatbot=graph.compile(checkpointer=checkpointer)
