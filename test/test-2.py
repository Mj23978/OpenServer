from langchain.chains import RetrievalQA
from langchain.chat_models import google_palm
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import chroma
from langchain.document_loaders import TextLoader

loader = TextLoader("./test/state_of_union.txt", encoding="utf-8")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

model_name = "BAAI/bge-small-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
)

db = chroma.Chroma.from_documents(docs, embeddings)
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)

docs[0]

palm_client = google_palm.ChatGooglePalm(google_api_key='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')

qa = RetrievalQA.from_chain_type(
    llm=palm_client,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={'k': 10})
)

print(qa.run('What did the president say about Ketanji Brown Jackson?'))