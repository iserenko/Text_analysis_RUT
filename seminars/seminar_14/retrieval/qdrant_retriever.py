from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter as QdrantFilter
from sentence_transformers import SentenceTransformer


@dataclass
class RetrievedChunk:
    chunk_id: str
    doc_id: str
    text: str
    score: float
    metadata: Dict[str, Any]


class QdrantRetriever:
    def __init__(
        self,
        qdrant_client: QdrantClient,
        collection_name: str,
        embedder: SentenceTransformer,
        default_top_k: int = 5,
    ):
        self.qdrant = qdrant_client
        self.collection = collection_name
        self.embedder = embedder
        self.default_top_k = default_top_k

    def _embed_query(self, query: str) -> List[float]:
        vec = self.embedder.model.encode(query, normalize_embeddings=True)
        return vec.tolist()

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        score_threshold: Optional[float] = None,
        qdrant_filter: Optional[QdrantFilter] = None,
    ) -> List[RetrievedChunk]:
        if top_k is None:
            top_k = self.default_top_k

        query_vec = self._embed_query(query)

        results = self.qdrant.query_points(
            collection_name=self.collection,
            query=query_vec,
            limit=top_k,
            with_payload=True,
            query_filter=qdrant_filter,
        )

        chunks: List[RetrievedChunk] = []

        for r in results.points:
            if score_threshold is not None and r.score < score_threshold:
                continue

            payload: Dict[str, Any] = r.payload or {}

            text = payload.get("text", "")
            doc_id = payload.get("doc_id", "")
            chunk_id = payload.get("chunk_id", r.id)

            chunks.append(
                RetrievedChunk(
                    chunk_id=str(chunk_id),
                    doc_id=str(doc_id),
                    text=text,
                    score=r.score,
                    metadata=payload,
                )
            )

        return chunks
