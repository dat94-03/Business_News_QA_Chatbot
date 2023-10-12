import streamlit as st
from streamlit_chat import message
import random
import time
# python -m streamlit run source/testUI.py

st.subheader("StockBot")
st.session_state['responses'] = ["Tôi có thể giúp gì cho bạn?"]
st.session_state['requests'] =[]
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
    print(query)
    if query:
        with st.spinner("typing..."):

            # get response from model GPT
            # time.sleep(3)
            response = str(random.randint(0,100))
        # add query and response to session state
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)
        print(st.session_state['responses'])
        print(st.session_state["requests"])


with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user') 