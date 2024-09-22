from dataclasses import dataclass


@dataclass
class PrototypeArticleStem:
    prototype_article_id: int
    stem_id: int
    occurrences: int
    nouniness: float
    verbiness: float

    id: int = 0
