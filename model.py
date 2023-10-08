from langchain.document_loaders import DirectoryLoader
from langchain.llms import GPT4All
from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.embeddings.gpt4all import GPT4AllEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.prompts.chat import ChatPromptTemplate

import chainlit as cl
import requests
import zipfile
import io
import os
import shutil

@cl.cache
def load_chain():
  github_archive_url = f'https://github.com/Crazzygamerr/Tadpole-Docs/archive/main.zip'

  response = requests.get(github_archive_url)
  if response.status_code == 200:
      zip_content = io.BytesIO(response.content)
      # if the folder is already present, delete it
      if os.path.exists('Tadpole-Docs'):
          shutil.rmtree('Tadpole-Docs')
      with zipfile.ZipFile(zip_content, 'r') as zip_ref:
          zip_ref.extractall()
      
      print(f"Repository 'Tadpole-Docs' downloaded and extracted successfully.")
  else:
      print(f"Failed to download repository. Status code: {response.status_code}")


  template = """Answer the question based only on the following context:
  {context}

  Question: {question}
  """
  prompt = ChatPromptTemplate.from_template(template)

  embeddings_model = GPT4AllEmbeddings()
  loader = DirectoryLoader('./Tadpole-Docs-main', glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
  documents = loader.load()
  text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
  texts = text_splitter.split_documents(documents)
  docsearch = Chroma.from_documents(texts, embeddings_model)
  retriever=docsearch.as_retriever()

  llm = GPT4All(model="wizardlm-13b-v1.1-superhot-8k.ggmlv3.q4_0.bin", n_threads=6, n_predict=512, streaming=True)
  chain = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever
  )
  
  return chain

chain = load_chain()

@cl.on_message
async def main(message):
    res = await cl.make_async(chain.run)(message, callbacks=[cl.LangchainCallbackHandler()])
    
    await cl.Message(content=f"{res}").send()
