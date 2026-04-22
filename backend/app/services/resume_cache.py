from dataclasses import dataclass
from typing import Generic, TypeVar

from app.services.hash_utils import hash_bytes
from app.services.pdf_text_extractor import PdfTextExtraction, extract_text_from_pdf
from app.services.resume_text_cleaner import clean_resume_text


T = TypeVar("T")


@dataclass(frozen=True)
class CachedParsedResume:
    resume_hash: str
    raw_text: str
    cleaned_text: str
    page_count: int


@dataclass(frozen=True)
class CacheLookup(Generic[T]):
    value: T
    hit: bool


class SimpleMemoryCache:
    def __init__(self, max_items: int = 128) -> None:
        self.max_items = max_items
        self._items: dict[str, object] = {}

    def get(self, key: str) -> object | None:
        return self._items.get(key)

    def set(self, key: str, value: object) -> None:
        if len(self._items) >= self.max_items:
            oldest_key = next(iter(self._items))
            self._items.pop(oldest_key, None)
        self._items[key] = value


parsed_resume_cache = SimpleMemoryCache(max_items=128)
match_result_cache = SimpleMemoryCache(max_items=128)


def get_or_parse_resume(file_content: bytes) -> CacheLookup[CachedParsedResume]:
    resume_hash = hash_bytes(file_content)
    cached = parsed_resume_cache.get(resume_hash)
    if isinstance(cached, CachedParsedResume):
        return CacheLookup(value=cached, hit=True)

    extraction: PdfTextExtraction = extract_text_from_pdf(file_content)
    parsed = CachedParsedResume(
        resume_hash=resume_hash,
        raw_text=extraction.raw_text,
        cleaned_text=clean_resume_text(extraction.raw_text),
        page_count=extraction.page_count,
    )
    parsed_resume_cache.set(resume_hash, parsed)
    return CacheLookup(value=parsed, hit=False)


def build_match_cache_key(resume_hash: str, jd_hash: str) -> str:
    return f"{resume_hash}:{jd_hash}"
