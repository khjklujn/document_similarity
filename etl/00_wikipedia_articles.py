import datetime
from typing import Dict, Tuple

import model
import repository
import util


config = util.Config()

topics = repository.prototype.Topic(config)
prototype_articles = repository.prototype.PrototypeArticle(config)
prototype_article_stems = repository.prototype.PrototypeArticleStem(config)
stems = repository.vocabulary.Stem(config)
words = repository.vocabulary.Word(config)

articles: Dict[str, Tuple] = {
    # 'Artificial Intelligence': (
    #     'Concept Mining',
    #     'Dictionary-based machine translation',
    #     'Distributional semantics',
    #     'Document classification',
    #     'Information extraction',
    #     'Latent Dirichlet allocation',
    #     'Latent semantic analysis',
    #     'Lexical analysis',
    #     'Natural language processing',
    #     'Sentiment analysis',
    #     'Text mining',
    #     'tf-idf',
    # ),
    # 'Uncategorized': (
    #     'Computational linguistics',
    #     'Content analysis',
    #     'Knowledge extraction',
    #     'Named-entity recognition',
    #     'Ontology learning',
    #     'Rule-based machine translation',
    #     'Semantic translation',
    #     'td-idf',
    #     'Topic model',
    # ),
    'Email Marketing': (
        'Content marketing',
        'Email marketing',
        'Personalized marketing',
    ),
}

for topic_name, pages in articles.items():
    for page_name in pages:
        topics.add(model.odoo.prototype.Topic(name=topic_name))
        topics.upsert_many()

        print(page_name, datetime.datetime.now())
        article = model.article.wikipedia.Article(page_name, config)

        print('  save article')
        prototype_articles.add(
            model.odoo.prototype.PrototypeArticle(
                topics.by_name(topic_name).id,
                article.name,
                article.unique_id,
                article.text_html,
                article.characterized_html
            )
        )
        prototype_articles.upsert_many()

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
            prototype_article_stems.add(
                model.odoo.prototype.PrototypeArticleStem(
                    prototype_articles.by_name(page_name)[0].id,
                    stems.by_name(stem).id,
                    counts['occurrences'],
                    counts['nouniness'],
                    counts['verbiness']
                )
            )
        prototype_article_stems.upsert_many()
