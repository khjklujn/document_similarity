from dataclasses import dataclass


@dataclass
class Word:
    stem_id: int
    name: str

    id: int = 0
    active: bool = True
