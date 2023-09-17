from llama_index.indices.loading import load_graph_from_storage
from llama_index.storage import StorageContext
import streamlit as st
import openai
openai.api_key= st.secrets['OPENAI_API_KEY']


# Create a storage context using the persist directory
storage_context = StorageContext.from_defaults(persist_dir='./storage')

# Load the graph from the storage context
graph = load_graph_from_storage(storage_context, root_id="APPL-23")
print(graph)

query_engine = graph.as_query_engine(child_branch_factor=1)
response = query_engine.query("What was the revenue at each quarter?")
print(response)