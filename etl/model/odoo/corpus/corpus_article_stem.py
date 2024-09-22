from dataclasses import dataclass


@dataclass
class CorpusArticleStem:
    corpus_article_id: int
    stem_id: int
    occurrences: int
    nouniness: float
    verbiness: float
    weight: float

    id: int = 0
