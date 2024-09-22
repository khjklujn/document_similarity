from dataclasses import dataclass


@dataclass
class LoadFailure:
    name: str
    unique_id: str
    category: str
    reason: str

    id: int = 0
