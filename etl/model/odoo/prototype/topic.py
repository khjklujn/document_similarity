from dataclasses import dataclass


@dataclass
class Topic:
    name: str
    active: bool = True

    id: int = 0

