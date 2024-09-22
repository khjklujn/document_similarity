from dataclasses import dataclass


@dataclass
class Year:
    name: str

    id: int = 0
    active: bool = True

