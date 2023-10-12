from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *
from source.apikey import apikey
import random
#   python -m streamlit run source/main.py


st.subheader("StockBot")

#Create first message
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["Tôi có thể giúp gì cho bạn?"]
#Collect first request
if 'requests' not in st.session_state:
    st.session_state['requests'] = []

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=apikey)

# Setup memorize the conversation
if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=1,return_messages=True)

system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question in Vietnamese as truthfully as possible using the provided context, 
and if the answer is not contained within the text below, say 'Tôi không biết'""")

human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory,prompt=prompt_template, llm=llm, verbose=True)

# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()

with textcontainer:
    if "my_text" not in st.session_state:
        st.session_state.my_text = ""

    def submit():
        '''Reset the input by updating the placeholder with a new input widget'''
        st.session_state.my_text = st.session_state.input
        st.session_state.input = ""
        
    st.text_input("Enter question here: ", key="input", on_change = submit)
    query = st.session_state.my_text
    
    # query = st.text_input("Query: ", key="input")
    if query:
        with st.spinner("typing..."):
            # find the context that matches the query
            results, context = find_match(query)
            
            # # get response from model GPT
            # response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
            response = str(random.randint(0,100))
            
        # add query and response to session state
        URL = f'''Tìm hiểu thêm tại: 1. {results['metadatas'][0][0]['URL']} 2. {results['metadatas'][0][1]['URL']} 3. {results['metadatas'][0][2]['URL']}'''
        st.session_state.requests.append(query)
        st.session_state.responses.append(response + '\n\n' + URL)
        
with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')     
        



          