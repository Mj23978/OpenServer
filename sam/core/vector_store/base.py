from abc import ABC
from enum import Enum
from typing import Any, Iterable, List, Optional, Tuple

from langchain.schema.vectorstore import VectorStore as Vector
from langchain.schema import Document


class VectorStore(ABC):

    client: Vector

    def add_documents(self, documents: List[Document], **kwargs: Any) -> List[str]:
        """Run more documents through the embeddings and add to the vectorstore.
        """
        texts: list[str] = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        return self.add_texts(texts=texts, metadatas=metadatas, **kwargs)

    def add_texts(
            self,
            texts: Iterable[str],
            metadatas: Optional[List[dict]] = None,
            **kwargs: Any,
    ) -> List[str]:
        return self.client.add_texts(texts=texts, metadatas=metadatas, kwargs=kwargs)

    def similarity_search(self, query: str, top_k: int, metadata: Optional[dict] = None, **kwargs: Any) -> List[Document]:
        return self.client.similarity_search(query=query, top_k=top_k, metadata=metadata, kwargs=kwargs)

    def similarity_search_with_relevance_scores(self, query: str, top_k: int, score_threshold: float, **kwargs: Any) -> List[Tuple[Document, float]]:
        return self.client.similarity_search_with_relevance_scores(query=query, top_k=top_k, score_threshold=score_threshold, kwargs=kwargs)

    def delete_embeddings_from_vector_db(self, ids: List[str]) -> bool | None:
        return self.client.delete(ids=ids)



class VectorStoreType(Enum):
    CHROMADB = "chromadb"
    LANCEDB = "lancedb"
    MILVUS = "milvus"
    PINECONE = "pinecone"
    QDRANT = "qdrant"
    REDIS = "redis"
    WEAVIATE = "weaviate"
    
    @classmethod
    def get_type(cls, type: str):
        type_enum_value = None
        for enum_value in VectorStoreType:
            if type == enum_value.value:
                type_enum_value=enum_value
                break
        return type_enum_value or cls.LANCEDB