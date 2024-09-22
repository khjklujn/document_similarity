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
stems = repository.vocabulary.Stem(config)
words = repository.vocabulary.Word(config)
years = repository.corpus.Year(config)

corpora.add(model.odoo.corpus.Corpus(name='Artificial Intelligence'))
corpora.upsert_many()

count = 0
for path, _, articles in os.walk(config.source_root):
    if not (
        '/AME/' in path or
        '/IJRM/' in path or
        '/JAMS/' in path or
        '/JCB/' in path or
        '/JCP/' in path or
        '/JM/' in path or
        '/JMR/' in path or
        '/JPPM/' in path or
        '/JR/' in path or
        '/MS/' in path
    ):
        continue
    for article_name in articles:
        if article_name.endswith('.pdf'):
            source_file = os.path.join(path, article_name)

            stats = os.stat(source_file)
            # if datetime.datetime.fromtimestamp(stats.st_mtime) <= datetime.datetime(2020, 1, 1) or datetime.datetime.fromtimestamp(stats.st_mtime) > datetime.datetime(2020, 3, 1):
            #     continue

            if 'Singh et al MS 2011' not in source_file:
                continue

            count += 1
            print(count, source_file, datetime.datetime.now(), datetime.datetime.fromtimestamp(stats.st_mtime))
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
