from langchain_community.document_loaders.text import TextLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import  SentenceTransformerEmbeddings
import os

# Tải dữ liệu từ các file txt và lưu trữ trong 1 mảng document
def load_data(list_path):
   documents = []
   for path in os.listdir(list_path):
       filename = os.path.join(list_path,path)
       loader = TextLoader(file_path=filename,encoding='utf-8')
       data = loader.load()
       documents.append(data)
   return documents

# Chia tài liệu thành các chunk
def split_data(data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=350,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )
    texts = []
    for i in range(len(data)) :
        text = text_splitter.split_documents(data[i])
        texts.append(text)
    return texts

# Mã hóa đoạn text đã chia thành các vecto embedding

def create_db(data,embedding_function):
   data_spliter = split_data(data)
   data_spliter_list = []
   for sublist in data_spliter:
       data_spliter_list.extend(sublist)
   db = Chroma.from_documents(data_spliter_list,embedding_function)
   return db



