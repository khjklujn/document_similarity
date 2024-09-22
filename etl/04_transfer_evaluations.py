from openpyxl import load_workbook

import model
import repository
import util


config = util.Config()

corpus_articles = repository.corpus.CorpusArticle(config)
workbook = load_workbook('/media/sf_dev/Downloads/Keyword Results.xlsx')
sheet = workbook.active
for index, row in enumerate(sheet):
    if index == 0:
        continue

    article_id = row[0].value
    on_topic = row[7].value
    print(article_id, on_topic)

    if on_topic and 'yes' in on_topic.lower():
        training_status = 'On Topic'
    elif on_topic and 'no' in on_topic.lower():
        training_status = 'Off Topic'

    corpus_article = corpus_articles.by_id(article_id)
    update = model.odoo.corpus.CorpusArticle(
        corpus_article.corpus_id,
        corpus_article.name,
        corpus_article.source_file,
        corpus_article.unique_id,
        corpus_article.united_status,
        corpus_article.tokenized,
        corpus_article.characterized,
        corpus_article.journal_id,
        corpus_article.year_id,
        training_status=training_status,
        read_status=corpus_article.read_status,
        category='Keyword',
        percent_about=corpus_article.percent_about
    )
    corpus_articles.add(update)
    corpus_articles.upsert_many()

# with open('article_reviews.txt', 'r') as file_in:
#     file_in.readline()
#     for line in file_in:
#         print([field.strip() for field in line.split('\t')])
#         (
#             title,
#             article_id,
#             on_topic,
#             level
#         ) = [field.strip() for field in line.split('\t')]

#         if on_topic:
#             print(title, on_topic)

#             unique_id = get_unique_id(int(article_id), config)
#             status = 'On Topic' if on_topic == 'Yes' else 'Off Topic'
#             percent_about = float(level) if level else None

#             corpus_article = corpus_articles.by_unique_id(unique_id)
#             print('  ', corpus_article.name)
#             update = model.odoo.corpus.CorpusArticle(
#                 corpus_article.corpus_id,
#                 corpus_article.name,
#                 corpus_article.source_file,
#                 corpus_article.unique_id,
#                 corpus_article.tokenized,
#                 corpus_article.characterized,
#                 corpus_article.journal_id,
#                 corpus_article.year_id,
#                 training_status=status,
#                 percent_about=percent_about
#             )
#             corpus_articles.add(update)
#             corpus_articles.upsert_many()
