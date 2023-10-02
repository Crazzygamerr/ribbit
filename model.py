from langchain.chains import LLMChain, APIChain
from langchain.chains.api.prompt import API_URL_PROMPT
from langchain.llms import GPT4All
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

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

system_template = """Use the following pieces of context to answer the users question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.
The "SOURCES" part should be a reference to the source of the document from which you got your answer.

And if the user greets with greetings like Hi, hello, How are you, etc reply accordingly as well.

Example of your response should be:

The answer is foo
SOURCES: xyz


Begin!
----------------
{summaries}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]
prompt = ChatPromptTemplate.from_messages(messages)
chain_type_kwargs = {"prompt": prompt}
# texts = text_splitter.split_text(text)

# # Create a metadata for each chunk
# metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]

# # Create a Chroma vector store
embeddings_model = GPT4AllEmbeddings()
loader = TextLoader("./api.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)
docsearch = Chroma.from_documents(texts, embeddings_model)

llm = GPT4All(
		model="orca-mini-3b.ggmlv3.q4_0.bin", 
		allow_download=True
)
chain = RetrievalQA.from_chain_type(
  llm=llm, 
  chain_type="stuff", 
  retriever=docsearch.as_retriever()
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
    cb = cl.AsyncLangchainCallbackHandler()

    res = await chain.acall(message, callbacks=[cb])
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