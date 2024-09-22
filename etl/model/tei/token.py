from dataclasses import dataclass

from ruamel.yaml import yaml_object  # type: ignore


from nltk.stem import PorterStemmer
import spacy

from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Token:
    text: str
    stem: str
    token: str
    part_of_speech: str
    dependency: str
    noun_value: float
    verb_value: float

    ps = PorterStemmer()

    @classmethod
    def from_token(cls, word: spacy.tokens.Token):
        stem = cls.ps.stem(word.text).lower()

        noun_value = 0.0
        verb_value = 0.0
        if word.pos_ == 'ADJ':
            noun_value = 0.25
        elif word.pos_ == 'ADV':
            verb_value = 0.25
        elif word.pos_ in ('NOUN', 'PROPN'):
            if 'subj' in word.dep_ or word.dep_ == 'ROOT':
                noun_value = 1.0
            else:
                noun_value = 0.5
        elif word.pos_ == 'VERB':
            if word.dep_ == 'ROOT':
                verb_value = 1
            else:
                verb_value = 0.5

        return cls(
            text=word.text,
            stem=stem,
            token=word,
            part_of_speech=word.pos_,
            dependency=word.dep_,
            noun_value=noun_value,
            verb_value=verb_value
        )

    @property
    def characterized_html(self):
        if (
            len(self.text) > 1 and
            self.noun_value > 0.0
        ):
            return f'<font color="#007F00">{self.stem}</font>'
        elif (
            len(self.text) > 1 and
            self.verb_value > 0.0
        ):
            return f'<font color="#7F0000">{self.stem}</font>'
        else:
            return f'<font color="#CFCFCF">{self.stem}</font>'
        # if (
        #     len(self.text) > 1 and
        #     self.noun_value > 0.0
        # ):
        #     return f'<font color="#007F00">({self.text} {self.part_of_speech})</b>'
        # elif (
        #     len(self.text) > 1 and
        #     self.verb_value > 0.0
        # ):
        #     return f'<font color="#7F0000">({self.text} {self.part_of_speech})</b>'
        # else:
        #     return f'<font color="#CFCFCF">({self.text} {self.part_of_speech})</font>'
