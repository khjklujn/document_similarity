from dataclasses import dataclass


@dataclass
class PrototypeArticleCorpusArticle:
    prototype_article_id: int
    topic_id: int
    corpus_article_id: int
    journal_id: int
    year_id: int
    distance: float
    divergence: float
    alpha: float
    beta: float

    id: int = 0
