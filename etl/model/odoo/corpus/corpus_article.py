from typing import Optional

from dataclasses import dataclass


@dataclass
class CorpusArticle:
    corpus_id: int
    name: str
    source_file: str
    unique_id: str
    united_status: str
    tokenized: str
    characterized: str
    journal_id: int
    year_id: int

    id: int = 0
    active: bool = True
    read_status: str = 'Not Reviewed'
    training_status: str = 'Not Reviewed'
    category: Optional[str] = None
    percent_about: Optional[float] = None
