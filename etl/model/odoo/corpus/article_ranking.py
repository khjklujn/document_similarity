from dataclasses import dataclass


@dataclass
class ArticleRanking:
    corpus_article_id: int
    read_status: str
    united_status: str
    training_status: str
    category: str
    journal_id: int
    year_id: int
    distance: float
    rank: int

    id: int = 0
