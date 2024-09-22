from dataclasses import dataclass


@dataclass
class PrototypeArticle:
    topic_id: int
    name: str
    unique_id: str
    tokenized: str
    characterized: str

    id: int = 0
    active: bool = True
