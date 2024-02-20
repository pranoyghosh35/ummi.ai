import os
import streamlit as st
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def read_api_key(file_path):
    with open(file_path, 'r') as file:
        api_key = file.read().strip()  # Remove newline characters and leading/trailing whitespaces
    return api_key

def set_openai_api_key(api_key):
    os.environ["OPENAI_API_KEY"] = api_key

def load_docs(directory):
    loader = DirectoryLoader(directory, glob="**/*.txt")
    documents = loader.load()
    return documents

def split_documents_into_chunks(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    return texts

def select_embeddings():
    return OpenAIEmbeddings()

def create_vectorstore(texts, embeddings):
    return Chroma.from_documents(texts, embeddings)

def create_retriever(db):
    return db.as_retriever(search_type='similarity', search_kwargs={"k": 2})

def create_qa_chain(llm, retriever):
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=False)

def main():
    # Initialize an empty list to store chat history
    chat_history = []
    #chat_history =""
    
    # Read API key from api_key.txt file
    api_key_file = os.path.join(os.path.dirname(__file__), 'api_key.txt')
    api_key = read_api_key(api_key_file)

    # Set OpenAI API key in environment variable
    set_openai_api_key(api_key)

    # Directory where text files are stored
    directory = "QA_data/"

    # Load all the text files in the directory
    documents = load_docs(directory)

    # Split the documents into chunks
    texts = split_documents_into_chunks(documents)

    # Select embeddings
    embeddings = select_embeddings()

    # Create the vectorstore to use as the index
    db = create_vectorstore(texts, embeddings)

    # Expose the index in a retriever interface
    retriever = create_retriever(db)

    # Create instance to interact with OpenAI's language models
    llm = OpenAI()  # Instance to interact with OpenAI's language models. Default - GPT-3.5 Turbo

    # Create a chain to answer questions
    qa = create_qa_chain(llm, retriever)

    print("Welcome to MaQuery! I am Ummi. How can I help today?")
    print("\n\nE.g. Ask us: Which topics can you help me with?\nWho are you and who developed you?\n... \n\nSay TATA/BYE if we have to end the conversation. \n\n")
    query = input("\nYou:")
    i = 1
    while True:
        result = qa({"query": query, "chat_history": chat_history})
        fmt_str = ""  # Formatting to show every new sentence (.) in next line for long responses
        for x in result["result"].split('.'):
            fmt_str = fmt_str + x + "\n"
        print("\nMaQuery:", fmt_str)
        #chat_history = [(query, result["result"])]
        chat_history.extend([(query, result["result"])])
        #chat_history=chat_history+str(query)+" "+str(result["result"])
        #print("!!",chat_history,"!!")
        query = input("\nYou:")
        tmp = query.upper()
        ## The end of conversation can be long or short
        # Long -because maybe they liked info we're providing or couldn't find relevant info quickly
        # Short -didn't actually get much chance to use
        # we give different ending note based on plausible mood of user
        if "TATA" in tmp or "BYE" in tmp:
            if i < 2:
                print("No problem. Return anytime.")
            elif i > 15:
                print("Did we provide the information you were looking for? Kindly give feedback.")
            else:
                print("Always happy to serve. Best wishes for the day ahead")
            break
        i += 1

if __name__ == "__main__":
    main()
