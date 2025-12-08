from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

from .chunker import Chunk


@dataclass
class ChunkEmbedding:
    chunk_id: str
    doc_id: str
    text: str
    vector: np.ndarray
    metadata: Dict[str, Any]


class Embedder:
    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        device: Optional[str] = 'cuda',
        batch_size: int = 32,
        normalize: bool = True,
    ) -> None:
        self.model = SentenceTransformer(model_name, device=device)
        self.batch_size = batch_size
        self.normalize = normalize

    def embed_chunks(self, chunks: List[Chunk]) -> List[ChunkEmbedding]:
        if not chunks:
            return []

        texts = [c.text for c in chunks]
        meta_list = [c.metadata for c in chunks]

        vectors = self.model.encode(
            texts,
            batch_size=self.batch_size,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize,
            show_progress_bar=False,
        )

        result: List[ChunkEmbedding] = []
        for chunk, vec, meta in zip(chunks, vectors, meta_list):
            result.append(
                ChunkEmbedding(
                    chunk_id=chunk.chunk_id,
                    doc_id=chunk.doc_id,
                    text=chunk.text,
                    vector=vec.astype(np.float32),
                    metadata=meta,
                )
            )

        return result
