import datetime
import os

import model
import repository
import util


config = util.Config()

corpora = repository.corpus.Corpus(config)
corpus_articles = repository.corpus.CorpusArticle(config)
corpus_article_stems = repository.corpus.CorpusArticleStem(config)
journals = repository.corpus.Journal(config)
load_failures = repository.corpus.LoadFailure(config)
stems = repository.vocabulary.Stem(config)
words = repository.vocabulary.Word(config)
years = repository.corpus.Year(config)

corpora.add(model.odoo.corpus.Corpus(name='Artificial Intelligence'))
corpora.upsert_many()

count = 0
for failure_id, load_failure in load_failures.records.items():
    if load_failure.category == 'GROBID Parse':
        source_file = os.path.join(config.source_root, load_failure.name)

        count += 1
        print(count, source_file, datetime.datetime.now())
        article = model.article.tei.Article(source_file, config)

        if article.parsing_succeeded:
            journals.add(
                model.odoo.corpus.Journal(
                    article.journal
                )
            )
            journals.upsert_many()

            years.add(
                model.odoo.corpus.Year(
                    article.year
                )
            )
            years.upsert_many()

            print('  save article')
            corpus_articles.add(
                model.odoo.corpus.CorpusArticle(
                    1,
                    article.title.text.strip(),
                    article.file_name,
                    article.unique_id,
                    'Not Reviewed',
                    article.text_html.strip(),
                    article.characterized_html.strip(),
                    journals.by_name(article.journal).id,
                    years.by_name(article.year).id
                )
            )
            corpus_articles.upsert_many()

            print('  save stems')
            stems_and_words = article.stem_to_words
            for stem, _ in stems_and_words.items():
                stems.add(model.odoo.vocabulary.Stem(name=stem, weight=1.0))
            stems.upsert_many()

            print('  save words', len(stems_and_words))
            for stem, word_set in sorted(stems_and_words.items()):
                for word in word_set:
                    words.add(
                        model.odoo.vocabulary.Word(
                            stems.by_name(stem).id,
                            word
                        )
                    )
            words.upsert_many()

            stem_characterization = article.stem_characterization
            print('  save distribution')
            for stem, counts in article.stem_characterization.items():
                corpus_article_stems.add(
                    model.odoo.corpus.CorpusArticleStem(
                        corpus_articles.by_unique_id(article.unique_id).id,
                        stems.by_name(stem).id,
                        counts['occurrences'],
                        counts['nouniness'],
                        counts['verbiness'],
                        1.0
                    )
                )
            corpus_article_stems.upsert_many()

            load_failures.delete(failure_id)