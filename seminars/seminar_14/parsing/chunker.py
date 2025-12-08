from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List
from uuid import uuid4

from transformers import AutoTokenizer

from .base import ParsedDocument


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    metadata: Dict[str, Any]


class Chunker:
    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        max_tokens: int = 512,
        overlap: int = 128,
    ) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_tokens = max_tokens
        self.overlap = overlap

    def chunk(self, doc: ParsedDocument) -> List[Chunk]:
        tokens = self.tokenizer.encode(doc.text, add_special_tokens=False)
        chunks: List[Chunk] = []

        n = len(tokens)
        start = 0

        while start < n:
            end = min(start + self.max_tokens, n)
            token_slice = tokens[start:end]
            text = self.tokenizer.decode(token_slice)

            meta = {
                **doc.metadata,
                "chunk_start_token": start,
                "chunk_end_token": end,
            }

            chunks.append(
                Chunk(
                    chunk_id=str(uuid4()),
                    doc_id=doc.doc_id,
                    text=text,
                    metadata=meta,
                )
            )

            if end == n:
                break

            start = end - self.overlap # add chunks overlap

        return chunks
