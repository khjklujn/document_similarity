from nltk.stem import PorterStemmer
import spacy

from model.article.node import Node

from . import dependency_map


class Token(Node):
    index: float
    _stemmer = PorterStemmer()

    @classmethod
    def walk_sentence(cls, parent: Node, token: spacy.tokens.Token):
        if token.dep_:
            root = dependency_map.dependency_map[token.dep_](parent, token)
            for child in token.children:
                root.walk_sentence(root, child)

    def __init__(self, parent: Node, token: spacy.tokens.Token):
        super().__init__(parent)

        self._token = token
        self._stem = self._stemmer.stem(token.text.lower())
        self._depth = self.parent.depth + 1

    def dependency_to_words(self, accumulator: dict) -> dict:
        if self.is_characterizing:
            if self.token.dep_ not in accumulator:
                accumulator[self.token.dep_] = set()
            accumulator[self.token.dep_].add(self.token.text.lower())
            for child in self.children:
                child.dependency_to_words(accumulator)
        return accumulator

    def lemma_characterization(self, accumulator: dict) -> dict:
        if self.is_characterizing:
            self.accumulate(
                self.token.lemma_.lower(),
                accumulator,
                start_value=0.0 + 0.0j,
                increment=complex(self.nouniness, self.verbiness)
            )

        for child in self.children:
            child.lemma_characterization(accumulator)
        return accumulator

    def lemma_to_words(self, accumulator: dict) -> dict:
        if self.is_characterizing:
            if self.token.lemma_.lower() not in accumulator:
                accumulator[self.token.lemma_.lower()] = set()
            accumulator[self.token.lemma_.lower()].add(self.token.text.lower())
            for child in self.children:
                child.lemma_to_words(accumulator)
        return accumulator

    def stem_characterization(self, accumulator: dict) -> dict:
        if self.is_characterizing:
            if self.stem not in accumulator:
                accumulator[self.stem] = {
                    'occurrences': 0,
                    'nouniness': 0.0,
                    'verbiness': 0.0
                }

            accumulator[self.stem]['occurrences'] += 1
            accumulator[self.stem]['nouniness'] += self.nouniness
            accumulator[self.stem]['verbiness'] += self.verbiness

        for child in self.children:
            child.stem_characterization(accumulator)

        return accumulator

    def stem_to_words(self, accumulator: dict) -> dict:
        if self.is_characterizing:
            if self.stem not in accumulator:
                accumulator[self.stem] = set()
            accumulator[self.stem].add(self.token.text.lower())

        for child in self.children:
            child.stem_to_words(accumulator)

        return accumulator

    @property
    def characterized_html(self) -> str:
        if self.nouniness > 0.5:
            return f'<b>{self.token.text}</b>'
        elif self.nouniness > 0.25:
            return self.token.text
        elif self.nouniness > 0.0:
            return f'<font color="#5F5F5F">{self.token.text}</font>'
        elif self.verbiness > 0.5:
            return f'<b><i>{self.token.text}</i></b>'
        elif self.verbiness > 0.1:
            return f'<i>{self.token.text}</i>'
        elif self.verbiness > 0.0:
            return f'<i><font color="#5F5F5F">{self.token.text}</font></i>'
        else:
            return f'<font color="#DFDFDF">{self.token.text}</font>'

    @property
    def is_characterizing(self) -> bool:
        return (
            self.token.pos_ in ('ADJ', 'ADV', 'NOUN', 'PROPN', 'VERB') and
            len(self.token.text) > 1 and
            self.token.text not in ('et', 'al')
        )

    @property
    def nouniness(self) -> float:
        if self.is_characterizing:
            if self.token.pos_ in ('NOUN', 'PROPN') and ('subj' in self.token.dep_ or self.token.dep_ == 'ROOT'):
                return 1.0
            elif self.token.pos_ in ('NOUN', 'PROPN'):
                return 0.5
            elif self.token.pos_ == 'ADJ':
                return 0.25
            else:
                return 0.0
        else:
            return 0.0

    @property
    def original_order(self):
        ret = [(self.token.i, self)]
        for child in self.children:
            ret += child.original_order
        return ret

    @property
    def stem(self):
        return self._stem

    @property
    def text_html(self):
        return self.token.text

    @property
    def token(self) -> spacy.tokens.Token:
        return self._token

    @property
    def verbiness(self) -> float:
        if self.is_characterizing:
            if self.token.pos_ == 'VERB' and self.token.dep_ == 'ROOT':
                return 1.0
            elif self.token.pos_ == 'VERB':
                return 0.5
            elif self.token.pos_ == 'ADV':
                return 0.1
            else:
                return 0.0
        else:
            return 0.0
