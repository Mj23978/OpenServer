import numpy as np

from langchain.embeddings.cohere import CohereEmbeddings

documents = [
    "Pizza is a dish.",
    "Paris is the capital of France",
    "numpy is a lib for linear algebra",
]
query = "Where is Paris?"

# embeddingProvider = GradientEmbeddings(
#   model="bge-large",
#   gradient_access_token="T5wu8hE0bMzTO2UIxuxyyAobBWsr4JWA",
#   gradient_workspace_id="723037f6-6a81-46ef-9d4a-9e8c27b50a93_workspace",
# )
embeddingProvider = CohereEmbeddings(
    model="embed-english-v2.0",
    cohere_api_key="",
)

documents_embedded = embeddingProvider.embed_documents(documents)
query_result = embeddingProvider.embed_query(query)


scores = np.array(documents_embedded) @ np.array(query_result).T
res = dict(zip(documents, scores))

print(scores)
print(res)
