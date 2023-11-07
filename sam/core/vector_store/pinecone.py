from langchain.vectorstores.pinecone import Pinecone
from pinecone.index import Index

from sam.core.vector_store.base import VectorStore
from sam.core.vector_store.embedding.base import BaseEmbedding


class PineconeVectorStore(VectorStore):
    def __init__(
            self,
            index: Index,
            namespace: str,
            embedding_model: BaseEmbedding,
            text_field: str = "text",
    ):

        self.namespace = namespace
        self.embedding_model = embedding_model
        self.text_field = text_field

        self.client = Pinecone(
            index=index,
            embedding=embedding_model.client,
            namespace=namespace,
            text_key=text_field,
        )
