from dataclasses import dataclass


@dataclass
class Stem:
    name: str
    weight: float

    id: int = 0
    active: bool = True
