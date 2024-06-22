from Prompt import prompt
from langchain_cohere import ChatCohere
from dotenv import load_dotenv
from Rag import retriever
from langchain_core.runnables import RunnablePassthrough
from Prompt import prompt
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

model = ChatCohere(model="command-r")
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
chain = (
    {"context": retriever | format_docs,"question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

x = chain.invoke("Cho tôi thông tin về thành phố Đà Nẵng?")
print(x)