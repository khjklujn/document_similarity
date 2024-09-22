from openpyxl import load_workbook

import model
import repository
import util


config = util.Config()

corpus_articles = repository.corpus.CorpusArticle(config)
workbook = load_workbook('United Seed Iteration 1.xlsx')
sheet = workbook.active
for index, row in enumerate(sheet):
    if index == 0:
        continue

    title = row[4].value
    status = row[1].value
    training = row[2].value

    if status != 'Not Reviewed' or training is not None:
        print(title)
        articles = corpus_articles.by_name(title)
        corpus_article = articles[0]

        if training and 'yes' in training.lower():
            training = 'On Topic'
        elif training and 'no' in training.lower():
            training = 'Off Topic'
        else:
            training = 'Not Reviewed'

        if status and 'prototype' in status.lower():
            status = 'New Prototype'
        elif status and 'antitype' in status.lower():
            status = 'New Antitype'

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
            training_status=training,
            read_status=status,
            category=corpus_article.category,
            percent_about=corpus_article.percent_about
        )
        corpus_articles.add(update)
        corpus_articles.upsert_many()
