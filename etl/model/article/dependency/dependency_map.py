from .adjectival_clause import AdjectivalClause
from .adjectival_complement import AdjectivalComplement
from .adjectival_modifier import AdjectivalModifier
from .adverbial_clause_modifier import AdverbialClauseModifier
from .adverbial_modifier import AdverbialModifier
from .agent import Agent
from .appositional_modifier import AppositionalModifier
from .attribute import Attribute
from .auxiliary import Auxiliary
from .auxiliary_passive import AuxiliaryPassive
from .case_marking import CaseMarking
from .classifier import Classifier
from .clausal_complement import ClausalComplement
from .clausal_subject import ClausalSubject
from .clausal_subject_passive import ClausalSubjectPassive
from .complement_of_preposition import ComplementOfPreposition
from .compound import Compound
from .conjunct import Conjunct
from .coordinating_conjunction import CoordinatingConjunction
from .copula import Copula
from .dative import Dative
from .determiner import Determiner
from .direct_object import DirectObject
from .discourse_element import DiscourseElement
from .dislocated_elements import DislocatedElements
from .expletive import Expletive
from .fixed_multiword_expression import FixedMultiwordExpression
from .flat_multiword_expression import FlatMultiwordExpression
from .goes_with import GoesWith
from .indirect_object import IndirectObject
from .interjection import Interjection
from .list import List
from .marker import Marker
from .meta_modifier import MetaModifier
from .modifier_of_nominal import ModifierOfNominal
from .modifier_of_quantifier import ModifierOfQuantifier
from .negation_modifier import NegationModifier
from .nominal_modifier import NominalModifier
from .nominal_subject import NominalSubject
from .nominal_subject_passive import NominalSubjectPassive
from .noun_compound_modifier import NounCompoundModifier
from .noun_phrase_as_adverbial_modifier import NounPhraseAsAdverbialModifier
from .numeric_modifier import NumericModifier
from .object import Object
from .object_of_preposition import ObjectOfPreposition
from .object_predicate import ObjectPredicate
from .oblique_nominal import ObliqueNominal
from .open_clausal_complement import OpenClausalComplement
from .orphan import Orphan
from .overridden_disfluency import OverriddenDisfluency
from .parataxis import Parataxis
from .particle import Particle
from .possession_modifier import PossessionModifier
from .pre_correlative_conjunction import PreCorrelativeConjunction
from .prepositional_modifier import PrepositionalModifier
from .punctuation import Punctuation
from .relative_clause_modifier import RelativeClauseModifier
from .root import Root
from .unclassified_dependent import UnclassifiedDependent
from .vocative import Vocative

dependency_map = {
    'acl': AdjectivalClause,
    'acomp': AdjectivalComplement,
    'advcl': AdverbialClauseModifier,
    'advmod': AdverbialModifier,
    'agent': Agent,
    'amod': AdjectivalModifier,
    'appos': AppositionalModifier,
    'attr': Attribute,
    'aux': Auxiliary,
    'auxpass': AuxiliaryPassive,
    'case': CaseMarking,
    'cc': CoordinatingConjunction,
    'ccomp': ClausalComplement,
    'clf': Classifier,
    'compound': Compound,
    'conj': Conjunct,
    'cop': Copula,
    'csubj': ClausalSubject,
    'csubjpass': ClausalSubjectPassive,
    'dative': Dative,
    'dep': UnclassifiedDependent,
    'det': Determiner,
    'predet': Determiner,
    'dobj': DirectObject,
    'discourse': DiscourseElement,
    'dislocated': DislocatedElements,
    'expl': Expletive,
    'fixed': FixedMultiwordExpression,
    'flat': FlatMultiwordExpression,
    'goeswith': GoesWith,
    'iobj': IndirectObject,
    'intj': Interjection,
    'list': List,
    'mark': Marker,
    'meta': MetaModifier,
    'neg': NegationModifier,
    'nmod': NominalModifier,
    'nn': NounCompoundModifier,
    'nounmod': ModifierOfNominal,
    'npadvmod': NounPhraseAsAdverbialModifier,
    'npmod': NounPhraseAsAdverbialModifier,
    'nsubj': NominalSubject,
    'nsubjpass': NominalSubjectPassive,
    'nummod': NumericModifier,
    'oprd': ObjectPredicate,
    'obj': Object,
    'obl': ObliqueNominal,
    'orphan': Orphan,
    'parataxis': Parataxis,
    'pcomp': ComplementOfPreposition,
    'pobj': ObjectOfPreposition,
    'poss': PossessionModifier,
    'preconj': PreCorrelativeConjunction,
    'prep': PrepositionalModifier,
    'prt': Particle,
    'punct': Punctuation,
    'quantmod': ModifierOfQuantifier,
    'relcl': RelativeClauseModifier,
    'reparandum': OverriddenDisfluency,
    'ROOT': Root,
    'vocative': Vocative,
    'xcomp': OpenClausalComplement
}
