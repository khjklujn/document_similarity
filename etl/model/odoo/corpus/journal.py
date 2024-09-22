from dataclasses import dataclass


@dataclass
class Journal:
    name: str

    id: int = 0
    active: bool = True

