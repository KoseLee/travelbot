from VectorDB import test
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings.sentence_transformer import  SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings
from dotenv import load_dotenv
import time
load_dotenv()
# Load_data
data = test.load_data(r'D:\Project_2-main\data')
# Tạo cơ sở vector để lưu trữ data
embedding_function = CohereEmbeddings()
vector_db = test.create_db(data,embedding_function)

# Tạo đối tượng retriver
retriever = vector_db.as_retriever( search_kwargs={"k": 4})







