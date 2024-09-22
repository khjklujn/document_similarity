from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet

import session
import util


def format_header(worksheet: Worksheet, names: tuple):
    worksheet.append(names)
    for cell in worksheet['1:1']:
        cell.font = Font(bold=True)


def get_distances(config: util.Config) -> list:
    query = """
    select
        articles_article_ranking.rank,
        articles_article_ranking.read_status,
        case
            when articles_article_ranking.training_status = 'On Topic' then 'Yes'
            when articles_article_ranking.united_status = 'Prototype' then 'Yes'
            when articles_article_ranking.training_status = 'Off Topic' then 'No'
            when articles_article_ranking.united_status = 'Antitype' then 'No'
            else null
        end training_status,
        articles_article_ranking.category,
        articles_corpus_article."name",
        articles_corpus_article.source_file,
        articles_journal."name",
        articles_year."name",
        articles_article_ranking.distance
    from articles_article_ranking
    inner join articles_corpus_article on
        articles_corpus_article.id = articles_article_ranking.corpus_article_id
    inner join articles_journal on
        articles_journal.id = articles_corpus_article.journal_id
    inner join articles_year on
        articles_year.id = articles_corpus_article.year_id
    order by
        articles_article_ranking.rank
    """
    with session.SLRV2(config) as slr_v2:
        return [
            (
                rank,
                status,
                training,
                category,
                article,
                float(distance),
                source_file,
                journal,
                year,
                source_file.split('/')[2],
                ' '.join(source_file.split('/')[-1].split('.')[0].split(' ')[:-2]),
            )
            for rank, status, training, category, article, source_file, journal, year, distance in slr_v2.session.execute(query).fetchall()
        ]


def get_sheet_1(workbook: Workbook, topic_name: str, config: util.Config):
    sheet = workbook.active

    format_header(
        sheet,
        (
            'Rank',
            'Status',
            'Training',
            'Category',
            'Article',
            'Distance',
            'Source',
            'Journal',
            'Year',
            'Issue',
            'Author',
        )
    )

    for record in get_distances(config):
        sheet.append(record)

    sheet.column_dimensions['E'].width = 100

    for index, cell in enumerate(sheet['F']):
        if index > 0:
            cell.style = 'Percent'

    for index, cell in enumerate(sheet['B']):
        if index > 0:
            if cell.value == 'Prototype':
                cell.font = Font(color='00AF00')
            elif cell.value == 'Antitype':
                cell.font = Font(color='AF0000')
            elif cell.value in ('New Antitype', 'New Prototype', 'On Topic', 'Off Topic'):
                pass
            else:
                cell.font = Font(color='CFCFCF')

    for index, cell in enumerate(sheet['C']):
        if index > 0:
            if cell.value == 'Yes':
                cell.font = Font(color='00AF00')
            elif cell.value == 'No':
                cell.font = Font(color='AF0000')
            else:
                cell.font = Font(color='CFCFCF')


if __name__ == '__main__':
    config = util.Config()
    topic_name = 'United With New'

    workbook = Workbook()

    get_sheet_1(workbook, topic_name, config)

    workbook.save(f'{topic_name} Iteration 26.xlsx')
