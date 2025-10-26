import streamlit as st
import os
from openai import OpenAI
from os import environ
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from langgraph.graph import START, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
import tempfile

template = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    
    Question: {question} 
    
    Context: {context} 
    
    Answer:
"""
prompt = PromptTemplate.from_template(template)

environ['OPENAI_API_KEY'] = os.environ["API_KEY"] 
environ['OPENAI_BASE_URL'] = 'https://api.ai.it.cornell.edu'

client = OpenAI(
	api_key=os.environ["API_KEY"],
	base_url="https://api.ai.it.cornell.edu",
)


st.title("📝 File Q&A with OpenAI")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md", "pdf"), accept_multiple_files= True)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

question = st.chat_input(
    "Ask something about the article",
    disabled=not uploaded_file,
)

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    retrieved_docs = vectorstore.similarity_search(state["question"], k=20)
    return {"context": retrieved_docs}




if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the article"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question and uploaded_file:
    # Read the content of the uploaded file
    document_list=[]
    for file in uploaded_file:
      
        
       
        if file.type =="application/pdf":
            
            temp_file_path= tempfile.NamedTemporaryFile(mode='w+b',suffix= ".pdf", delete=False)
            temp_file_path.write(file.read())
            temp_file_path.close()
            loader = PyPDFLoader(
                temp_file_path.name,
                mode="single",
            )
            document= loader.load()
            document_list.extend(document)

        
        else:
           
            document = Document(page_content=file.read().decode("utf-8"))
            document_list.append(document)
    
   
    chunk_size = 200
    chunk_overlap = 50
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )
    chunks = text_splitter.split_documents(document_list)
    vectorstore = Chroma.from_documents(documents=chunks, embedding=OpenAIEmbeddings(model="openai.text-embedding-3-large"))
    graph_builder = StateGraph(State).add_sequence([retrieve])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    result = graph.invoke({"question": question})

    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

   
    
    relevant_content= ""
    for d in result["context"]:
        relevant_content+=d.page_content



    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="openai.gpt-4o",  # Change this to a valid model name
            messages=[
               
                {"role": "system", "content": f"Your responses must be generated based on only this content:\n\n{relevant_content}. You can think logically based on your understanding of the content, but if there is no related information, simply reply I do not know"},
                *st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)
       

    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response})