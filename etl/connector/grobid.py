import requests

from lxml import etree


class Grobid:
    def __init__(self, url):
        self._url = url

    def close(self):
        pass

    def commit(self):
        pass

    def process_full_text(self, file_name):
        files = {
            'input': (
                file_name,
                open(file_name, 'rb'),
                'application/pdf',
                {'Expires': '0'}
            )
        }

        url = f'{self.url}/processFulltextDocument'

        result = requests.post(
            url=url,
            files=files,
            data={},
            headers={'Accept': 'application/xml'}
        )
        if result.text == '[NO_BLOCKS] PDF parsing resulted in empty content':
            return None

        with open('tei.xml', 'w') as file_out:
            file_out.write(result.text)

        return etree.fromstring(bytes(result.text.encode('utf-8')))

    @property
    def url(self):
        return self._url
