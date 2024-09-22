import model
import repository
import util


class State:
    corpus_articles = repository.corpus.CorpusArticle(util.Config())
    corpus_article_stems = repository.corpus.CorpusArticleStem(util.Config())
    stems = repository.vocabulary.Stem(util.Config())


def adjust_weight(
    on_topic: model.odoo.corpus.CorpusArticle,
    scale: float,
    state: State
):
    [
        state.stems.add(
            model.odoo.vocabulary.Stem(
                state.stems.by_id(stem.stem_id).name,
                float(state.stems.by_id(stem.stem_id).weight) * scale
            )
        )
        for stem in state.corpus_article_stems.by_corpus_article_id(on_topic.id)
    ]
    state.stems.upsert_many()


def process_new_prototypes(state: State):
    on_topics = state.corpus_articles.by_read_status('New Prototype')
    for on_topic in on_topics:
        print('New Prototype', on_topic.name)
        state.stems.reset()
        adjust_weight(on_topic, 2.0, state)


def process_new_antitypes(state: State):
    off_topics = state.corpus_articles.by_read_status('New Antitype')
    for off_topic in off_topics:
        print('New Antitype', off_topic.name)
        state.stems.reset()
        adjust_weight(off_topic, 1.0 / 2.0, state)


def promote_new_prototypes(state: State):
    articles = state.corpus_articles.by_read_status('New Prototype')
    for article in articles:
        state.corpus_articles.add(
            model.odoo.corpus.CorpusArticle(
                article.corpus_id,
                article.name,
                article.source_file,
                article.unique_id,
                article.united_status,
                article.tokenized,
                article.characterized,
                article.journal_id,
                article.year_id,
                article.id,
                article.active,
                'Prototype',
                article.training_status,
                article.category,
                article.percent_about
            )
        )
    state.corpus_articles.upsert_many()


def promote_new_antitypes(state: State):
    articles = state.corpus_articles.by_read_status('New Antitype')
    for article in articles:
        state.corpus_articles.add(
            model.odoo.corpus.CorpusArticle(
                article.corpus_id,
                article.name,
                article.source_file,
                article.unique_id,
                article.united_status,
                article.tokenized,
                article.characterized,
                article.journal_id,
                article.year_id,
                article.id,
                article.active,
                'Antitype',
                article.training_status,
                article.category,
                article.percent_about
            )
        )
    state.corpus_articles.upsert_many()


def main():
    state = State()

    process_new_prototypes(state)
    process_new_antitypes(state)

    promote_new_prototypes(state)
    promote_new_antitypes(state)


if __name__ == '__main__':
    main()
