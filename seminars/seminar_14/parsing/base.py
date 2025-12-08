from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
from abc import ABC, abstractmethod


@dataclass
class ParsedDocument:
    doc_id: str
    text: str
    metadata: Dict[str, Any]


class BaseParser(ABC):
    @abstractmethod
    def can_handle(self, path: Path) -> bool:
        raise NotImplementedError

    @abstractmethod
    def parse(self, path: Path | str) -> ParsedDocument:
        raise NotImplementedError
