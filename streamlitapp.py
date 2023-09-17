import streamlit as st 
import os
import openai
import llama_index
from llama_index.llms import OpenAI
from llama_index.indices.composability import ComposableGraph
from llama_index.storage import StorageContext
from llama_index import TreeIndex, SummaryIndex
from llama_index.indices.loading import load_graph_from_storage

from llama_index.indices.loading import load_graph_from_storage
from llama_index.storage import StorageContext
import streamlit as st
import openai
openai.api_key= st.secrets['OPENAI_API_KEY']


st.set_page_config(page_title="Chat with AAPL 23 10-Qs, powered by Munger", page_icon=":chart_with_upwards_trend:", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat with Munger :chart_with_upwards_trend: :eyeglasses:")

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Apple's 2023 financial documents!"}
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the AAPL 2023 10-Q docs – hang tight! This should take 1-2 minutes."):

        # Create a storage context using the persist directory
        storage_context = StorageContext.from_defaults(persist_dir='./storage')

        # Load the graph from the storage context
        graph = load_graph_from_storage(storage_context, root_id="APPL-23")

        query_engine = graph.as_query_engine(child_branch_factor=1)
        
        return query_engine

query_engine =load_data()

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_engine.query(prompt)
            #ipdb.set_trace()
            st.write(response.response)
            #st.code(response.get_formatted_sources())
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history        
