from __future__ import annotations
from typing import Optional


class Node:
    def __init__(self, parent: Optional[Node]):
        self._parent = None
        self._children: list = []
        self._depth = 0

        self.parent = parent

    def accumulate(self, key, dist: dict, start_value=0, increment=1):
        if key not in dist:
            dist[key] = start_value
        dist[key] += increment

    def add_child(self, child: Node):
        self._children.append(child)

    def dependency_to_words(self, accumulator: dict) -> dict:
        for child in self.children:
            child.dependency_to_words(accumulator)
        return accumulator

    def lemma_characterization(self, accumulator: dict) -> dict:
        for child in self.children:
            child.lemma_characterization(accumulator)
        return accumulator

    def lemma_to_words(self, accumulator: dict) -> dict:
        for child in self.children:
            child.lemma_to_words(accumulator)
        return accumulator

    def remove_child(self, child: Node):
        self._children.remove(child)

    def stem_characterization(self, accumulator: dict) -> dict:
        for child in self.children:
            child.stem_characterization(accumulator)
        return accumulator

    def stem_to_words(self, accumulator: dict) -> dict:
        for child in self.children:
            child.stem_to_words(accumulator)
        return accumulator

    def token_count(self, accumulator: dict) -> dict:
        for child in self.children:
            child.token_count(accumulator)
        return accumulator

    @property
    def children(self):
        return self._children

    @property
    def depth(self):
        return self._depth

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: Node):
        if self.parent:
            self.parent.remove_child(self)
        self._parent = parent
        if self.parent:
            self.parent.add_child(self)

    @property
    def walk(self):
        ret = [self]
        ret += [child.walk for child in self._children]

        return ret

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.__class__.__name__
