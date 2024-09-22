import os
import shutil

from openpyxl import load_workbook, Workbook


def get_filename(record: dict):
    (
        issue,
        issue_number,
        month,
        year
    ) = record['Issue'].split(' ')
    month_map = {
        'January': 'Jan',
        'February': 'Feb',
        'March': 'Mar',
        'April': 'Apr',
        'May': 'May',
        'June': 'Jun',
        'July': 'Jul',
        'August': 'Aug',
        'September': 'Sep',
        'October': 'Oct',
        'November': 'Nov',
        'December': 'Dec'
    }
    month_abbreviation = month_map.get(month, month)

    ret = (
        record['Journal'],
        f'{record["Year"]} {record["Journal"]}',
        f'Vol {record["Volume"]} {issue} {issue_number} {month_abbreviation} {year}',
        f'{record["Article"]}.pdf'
    )
    return os.path.join(*ret)


def check(file_name: str):
    if os.path.exists(
        os.path.join(
            '/media/sf_dev/Dropbox/Jerry GA/AI SLR Project Journal Update V2/',
            file_name
        )
    ):
        return os.path.join(
            '/media/sf_dev/Dropbox/Jerry GA/AI SLR Project Journal Update V2/',
            file_name
        )
    elif os.path.exists(
        os.path.join(
            '/media/sf_dev/Dropbox/AI and Marketing Articles 10 Years Top Journals/',
            file_name
        )
    ):
        return os.path.join(
            '/media/sf_dev/Dropbox/AI and Marketing Articles 10 Years Top Journals/',
            file_name
        )
    else:
        print(file_name)


def copy(source_file: str, file_name: str):
    directory = os.path.join(*file_name.split('/')[:-1])
    target_path = '/media/sf_dev/Downloads/Corpus/'
    if not os.path.exists(os.path.join(target_path, directory)):
        os.makedirs(os.path.join(target_path, directory))

    target_file = os.path.join(target_path, file_name)
    print(f'{source_file} ==> {target_file}')
    shutil.copy2(source_file, target_file)


def process_sheet(sheet: str, workbook: Workbook):
    sheet = workbook[sheet]
    header: list = []
    for index, row in enumerate(sheet):
        if index == 0:
            header = [cell.value.strip() for cell in row if cell.value]  # type: ignore
            continue
        values = [cell.value for cell in row]  # type: ignore
        if values[0]:
            record = dict(zip(header, values))

            file_name = get_filename(record)
            source_file = check(file_name)
            copy(source_file, file_name)


if __name__ == '__main__':
    sheets = (
        'JM_Update 6 25 20',
        'JAMS_Update 6 25 20',
        ' JMR_Update 6 25 20',
        ' IJRM_Update 6 25 20',
        'MS_Update 6 25 20',
        'JCB',
        'JCP',
        'JPPM',
        'JR',
        'AME'
    )
    workbook = load_workbook('Audit Doc V5 - 6 25 2020.xlsx')

    for sheet in sheets:
        process_sheet(sheet, workbook)
