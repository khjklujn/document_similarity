from dataclasses import dataclass


@dataclass
class Corpus:
    name: str

    id: int = 0
    active: bool = True

