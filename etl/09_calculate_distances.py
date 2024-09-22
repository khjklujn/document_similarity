import datetime

from kneed import KneeLocator
import numpy as np

import model
import repository
import util


np.seterr(divide='raise')


class State:
    corpus_articles = repository.corpus.CorpusArticle(util.Config())
    corpus_article_corpus_articles = repository.corpus.CorpusArticleCorpusArticle(util.Config())
    corpus_article_stems = repository.corpus.CorpusArticleStem(util.Config())
    stems = repository.vocabulary.Stem(util.Config())


def calculate_distance(prototype_article_id: int, corpus_article: model.odoo.corpus.CorpusArticle, state: State) -> float:
    prototype_stems = {
        stem.stem_id: complex(stem.nouniness, stem.verbiness)
        for stem in state.corpus_article_stems.by_corpus_article_id(prototype_article_id)
        if stem.occurrences > 1
    }
    prototype_weights = {
        stem_id: float(state.stems.by_id(stem_id).weight)
        for stem_id in prototype_stems
    }

    corpus_stems = {
        stem.stem_id: complex(stem.nouniness, stem.verbiness)
        for stem in state.corpus_article_stems.by_corpus_article_id(corpus_article.id)
        if stem.occurrences > 1
    }

    if len(corpus_stems) > 10:
        stems = sorted(set(prototype_stems.keys()) | set(corpus_stems.keys()))

        prototype_vector = np.array(
            [
                prototype_stems.get(stem_id, 1e-100 + 0.0j) * prototype_weights.get(stem_id, 1.0)
                for stem_id in stems
            ]
        )
        corpus_vector = np.array(
            [
                corpus_stems.get(stem_id, 1e-100 + 0.0j) * prototype_weights.get(stem_id, 1.0)
                for stem_id in stems
            ]
        )

        prototype_vector /= prototype_vector.sum()
        corpus_vector /= corpus_vector.sum()

        m = (corpus_vector + prototype_vector) / 2

        corpus_log2 = np.log2(corpus_vector / m)
        prototype_log2 = np.log2(prototype_vector / m)

        ksd = (
            (corpus_vector * corpus_log2).sum() +
            (prototype_vector * prototype_log2).sum()
        ) / 2

        return float(1.0 - (ksd.real**2 + ksd.imag**2))
    else:
        return 0.0


def process_prototype_article(prototype_article: model.odoo.corpus.CorpusArticle, corpus_id: int, state: State):
    print(prototype_article.name, datetime.datetime.now())
    similarities = [
        (
            calculate_distance(prototype_article.id, article, state),
            article.id,
            article.journal_id,
            article.year_id
        )
        for article in state.corpus_articles.by_corpus_id(corpus_id)
    ]

    similarities.sort()
    similarities.reverse()

    x = list(range(len(similarities)))
    y = [jenson_shannon for jenson_shannon, _, _, _ in similarities]
    kneedle = KneeLocator(x, y, S=1.0, curve='concave', direction='decreasing', online=True)
    alpha = float(kneedle.knee_y)
    beta = min(float(75 / alpha), 100.0)
    # beta = float(75 / alpha)

    count = 0
    for jenson_shannon, corpus_article_id, journal_id, year_id in similarities:
        distance = jenson_shannon * (
            (
                np.exp(beta * (jenson_shannon - alpha)) /
                (1.0 + np.exp(beta * (jenson_shannon - alpha)))
            )
        )

        state.corpus_article_corpus_articles.add(
            model.odoo.corpus.CorpusArticleCorpusArticle(
                prototype_article.id,
                corpus_article_id,
                journal_id,
                year_id,
                distance,
                jenson_shannon,
                alpha,
                beta
            )
        )

        if count % 200 == 0:
            print('  ', count, datetime.datetime.now())
            state.corpus_article_corpus_articles.upsert_many()
        count += 1

    state.corpus_article_corpus_articles.upsert_many()


def main():
    state = State()

    corpus_id = 1
    for index, article in enumerate(state.corpus_articles.by_read_status('Prototype')):
        print(index)
        process_prototype_article(article, corpus_id, state)


if __name__ == '__main__':
    main()
