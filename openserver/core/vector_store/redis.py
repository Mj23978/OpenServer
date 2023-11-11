import json
import re
import uuid
import numpy as np
import redis
from typing import Any, List, Iterable, Mapping, Optional
from langchain.schema import Document
from langchain.vectorstores.redis import Redis

from ..config.config import get_config
from .base import VectorStore
from .embedding.base import BaseEmbedding


DOC_PREFIX = "doc:"

CONTENT_KEY = "content"
METADATA_KEY = "metadata"
VECTOR_SCORE_KEY = "vector_score"


class RedisVectorStore(VectorStore):

    DEFAULT_ESCAPED_CHARS = r"[,.<>{}\[\]\\\"\':;!@#$%^&*()\-+=~\/ ]"

    def __init__(self, index: str, embedding_model: BaseEmbedding):
        """
        Args:
            index: An instance of a Redis index.
            embedding_model: An instance of a BaseEmbedding model.
            vector_group_id: vector group id used to index similar vectors.
        """
        redis_url = get_config('REDIS_URL')
        url = "redis://" + redis_url

        self.redis_client = redis.Redis.from_url(
            url, decode_responses=True)
        self.client = Redis(
            redis_url=url,
            index_name=index,
            embedding=embedding_model.client,
        )
        self.index = index
        self.embedding_model = embedding_model
        self.content_key = "content"
        self.metadata_key = "metadata"
        self.vector_key = "content_vector"

    def build_redis_key(self, prefix: str) -> str:
        """Build a redis key with a prefix."""
        return f"{prefix}:{uuid.uuid4().hex}"

    def add_texts(self, texts: Iterable[str],
                  metadatas: Optional[List[dict]] = None,
                  embeddings: Optional[List[List[float]]] = None,
                  ids: Optional[list[str]] = None,
                  **kwargs: Any) -> List[str]:
        pipe = self.redis_client.pipeline()
        prefix = DOC_PREFIX + str(self.index)
        keys = []
        for i, text in enumerate(texts):
            id = ids[i] if ids else self.build_redis_key(prefix)
            metadata = metadatas[i] if metadatas else {}
            embedding = self.embedding_model.get_embedding(text)
            embedding_arr = np.array(embedding, dtype=np.float32)

            pipe.hset(id, mapping={CONTENT_KEY: text, self.vector_key: embedding_arr.tobytes(),
                                   METADATA_KEY: json.dumps(metadata)})

            keys.append(id)
        pipe.execute()
        return keys

    def get_matching_text(self, query: str, top_k: int = 5, metadata: Optional[dict] = None, **kwargs: Any) -> List[Document]:

        embed_text = self.embedding_model.get_embedding(query)
        from redis.commands.search.query import Query
        hybrid_fields = self._convert_to_redis_filters(metadata)

        base_query = f"{hybrid_fields}=>[KNN {top_k} @{self.vector_key} $vector AS vector_score]"
        return_fields = [METADATA_KEY, CONTENT_KEY, "vector_score", 'id']
        query = (
            Query(base_query)
            .return_fields(*return_fields)
            .sort_by("vector_score")
            .paging(0, top_k)
            .dialect(2)
        )

        params_dict: Mapping[str, str] = {
            "vector": np.array(embed_text)
            .astype(dtype=np.float32)
            .tobytes()
        }

        results = self.redis_client.ft(self.index).search(query, params_dict)

        # Prepare document results
        documents: list[Document] = []
        for result in results.docs:
            documents.append(
                Document(
                    page_content=result.content,
                    metadata=json.loads(result.metadata)
                )
            )
        return documents

    def _convert_to_redis_filters(self, metadata: Optional[dict] = None) -> str:
        if metadata is not None:
            if len(metadata) == 0:
                return "*"
            filter_strings = []
            for key in metadata.keys():
                filter_string = "@%s:{%s}" % (key,
                                              self.escape_token(str(metadata[key])))
                filter_strings.append(filter_string)

            joined_filter_strings = " & ".join(filter_strings)
            return f"({joined_filter_strings})"
        return "*"

    def escape_token(self, value: str) -> str:
        escaped_chars_re = re.compile(Redis.DEFAULT_ESCAPED_CHARS)

        def escape_symbol(match: re.Match) -> str:
            return f"\\{match.group(0)}"

        return escaped_chars_re.sub(escape_symbol, value)
