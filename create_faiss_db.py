# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 20:57:14 2024

@author: laksh
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
import yaml
from langchain_openai import OpenAIEmbeddings

DB_FAISS_PATH = 'faiss_vectorstore/'


OPENAI_CONFIG_FILE = 'api_key.yaml'

with open(OPENAI_CONFIG_FILE, 'r') as f:
    config = yaml.safe_load(f)

apikey = config['openai']['access_key']




def load_documents(path):
    loader = DirectoryLoader(path, glob="**/*.txt", show_progress=True)
    documents = loader.load()
    
    return documents


# Create vector database
def create_vector_db():
    # Load retrieved content
    
    documents_eng = load_documents('./Kids_stories/English')
    documents_ml = load_documents('./Kids_stories/Malayalam')
    documents_hi = load_documents('./Kids_stories/Hindi')
    
    #print(documents_ml)
    print('\nNumber of English documents loaded: ', len(documents_eng))
    print('\nNumber of Hindi documents loaded: ', len(documents_hi))
    print('Number of Malayalam documents loaded: ', len(documents_ml), '\n')
    #loader = TextLoader("./Kids_stories/English/A Glass of Milk.txt")
    #documents = loader.load()
    
    documents_eng.extend(documents_ml)
    documents_eng.extend(documents_hi)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800,
                                                   chunk_overlap=100)
    texts = text_splitter.split_documents(documents_eng)
    print('\nNumber of pages created', len(texts), '\n')
    print(texts[100])
    
    #embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
     #                                  model_kwargs={'device': 'cpu'})
    
    embeddings = OpenAIEmbeddings(openai_api_key = apikey)

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    create_vector_db()
