from langchain.chains import LLMChain, APIChain
from langchain.document_loaders import DirectoryLoader
from langchain.chains.api.prompt import API_URL_PROMPT
from langchain.llms import GPT4All
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.gpt4all import GPT4AllEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

import chainlit as cl

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# # Create a Chroma vector store
embeddings_model = GPT4AllEmbeddings()
# loader = TextLoader("./api.txt")
loader = DirectoryLoader('./Tadpole-Docs', glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)
docsearch = Chroma.from_documents(texts, embeddings_model)
retriever=docsearch.as_retriever()

llm = GPT4All(model="ggml-model-gpt4all-falcon-q4_0.bin", allow_download=True)
chain = RetrievalQA.from_chain_type(
  llm=llm, 
  chain_type="stuff", 
  retriever=retriever
)


# @cl.on_chat_start
# async def on_chat_start():
    # files = None

    # # Wait for the user to upload a file
    # while files == None:
    #     files = await cl.AskFileMessage(
    #         content="Please upload a text file to begin!",
    #         accept=["text/plain"],
    #         max_size_mb=20,
    #         timeout=180,
    #     ).send()

    # file = files[0]

    # msg = cl.Message(
    #     content=f"Processing `{file.name}`...", disable_human_feedback=True
    # )
    # await msg.send()

    # # Decode the file
    # text = file.content.decode("utf-8")

    # # Split the text into chunks

    # Let the user know that the system is ready
    # msg.content = f"Processing `{file.name}` done. You can now ask questions!"
    # await msg.update()

    # cl.user_session.set("chain", chain)


@cl.on_message
async def main(message):
    # chain = cl.user_session.get("chain")  # type: ConversationalRetrievalChain
    # cb = cl.AsyncLangchainCallbackHandler()

    res = await chain.acall(message, )
    # answer = res["answer"]
    # source_documents = res["source_documents"]  # type: List[Document]

    # text_elements = []  # type: List[cl.Text]

    # if source_documents:
    #     for source_idx, source_doc in enumerate(source_documents):
    #         source_name = f"source_{source_idx}"
    #         # Create the text element referenced in the message
    #         text_elements.append(
    #             cl.Text(content=source_doc.page_content, name=source_name)
    #         )
    #     source_names = [text_el.name for text_el in text_elements]

    #     if source_names:
    #         answer += f"\nSources: {', '.join(source_names)}"
    #     else:
    #         answer += "\nNo sources found"

    await cl.Message(content=res['result']).send()