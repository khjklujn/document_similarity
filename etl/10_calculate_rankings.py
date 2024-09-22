import datetime

import model
import repository
import session
import util


def process_rankings(config: util.Config):
    query = """
    select
        articles_corpus_article.id,
        articles_corpus_article.read_status,
        articles_corpus_article.united_status,
        articles_corpus_article.training_status,
        articles_corpus_article.category,
        articles_corpus_article.journal_id,
        articles_corpus_article.year_id,
        1 - exp(sum(ln(1 + 1e-320 - articles_corpus_article_corpus_article.distance))) distance
    from articles_corpus_article prototype_article
    inner join articles_corpus_article_corpus_article on
        articles_corpus_article_corpus_article.prototype_article_id = prototype_article.id
    inner join articles_corpus_article on
        articles_corpus_article.id = articles_corpus_article_corpus_article.corpus_article_id
    where
        prototype_article.read_status = 'Prototype'
    group by
        articles_corpus_article.id,
        articles_corpus_article.read_status,
        articles_corpus_article.training_status,
        articles_corpus_article.category,
        articles_corpus_article.journal_id,
        articles_corpus_article.year_id
    order by
        distance desc
    """
    article_rankings = repository.corpus.ArticleRanking(config)
    with session.SLRV2(config) as slr_v2:
        for rank, record in enumerate(slr_v2.session.execute(query).fetchall()):
            (
                corpus_article_id,
                read_status,
                united_status,
                training_status,
                category,
                journal_id,
                year_id,
                distance
            ) = record

            article_rankings.add(
                model.odoo.corpus.ArticleRanking(
                    corpus_article_id,
                    read_status,
                    united_status,
                    training_status,
                    category,
                    journal_id,
                    year_id,
                    distance,
                    rank + 1
                )
            )
            if rank % 200 == 0:
                print(rank, datetime.datetime.now())
                article_rankings.upsert_many()

        article_rankings.upsert_many()


if __name__ == '__main__':
    config = util.Config()

    process_rankings(config)
