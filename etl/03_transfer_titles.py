import model
import repository
import session
import util


config = util.Config()

corpus_articles = repository.corpus.CorpusArticle(config)

query = """
select
    unique_id,
    replace(replace(replace(name, '''''', ''''), '%(', ' '), ')s', ' ')
from articles_corpus_article
"""

with session.SLRProd(config) as slr:
    titles = {
        sha512: title
        for sha512, title in slr.session.execute(query).fetchall()
    }

for sha512, title in titles.items():
    print(title)
    corpus_article = corpus_articles.by_unique_id(sha512)
    update = model.odoo.corpus.CorpusArticle(
        corpus_article.corpus_id,
        title,
        corpus_article.source_file,
        sha512,
        corpus_article.united_status,
        corpus_article.tokenized,
        corpus_article.characterized,
        corpus_article.journal_id,
        corpus_article.year_id
    )
    corpus_articles.add(update)
    corpus_articles.upsert_many()
