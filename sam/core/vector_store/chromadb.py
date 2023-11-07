
import chromadb
from chromadb.config import Settings
from chromadb.api import ClientAPI
from langchain.vectorstores.chroma import Chroma

from sam.core.vector_store.base import VectorStore
from sam.core.vector_store.embedding.base import BaseEmbedding


def build_chroma_client(host: str | None, port: str | None, persistance = False) -> ClientAPI:
    if persistance == True:
      return chromadb.PersistentClient()
    else :
        return chromadb.Client(Settings(
            chroma_api_impl="rest",
            chroma_server_host=host,
            chroma_server_http_port=port
        ))


class ChromaDBVectorStore(VectorStore):
    def __init__(
            self,
            client_options: ClientAPI,
            collection_name: str,
            embedding_model: BaseEmbedding,
    ):
        self.client_options = client_options
        self.collection_name = collection_name
        self.embedding_model = embedding_model

        self.client = Chroma(
            client=self.client_options,
            collection_name=collection_name,
            embedding_function=embedding_model.client,
        )
