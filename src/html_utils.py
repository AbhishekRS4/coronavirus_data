import urllib3
from bs4 import BeautifulSoup

class HTMLDataParser:
    def __init__(self, url_to_parse):
        self._soup = None
        self._table = None
        self._tables = None
        self._html_data = None
        self._table_rows = None
        self._html_status = None
        self._url_handler = None
        self._table_header = None
        self._url_to_parse = url_to_parse

    def init_url_parser(self):
        if self._html_data is None and self._html_status is None:
            self._url_handler = urllib3.PoolManager().urlopen("GET", self._url_to_parse)
            self._html_data = self._url_handler.data
            self._html_status = self._url_handler.status
        return

    def init_beautiful_soup(self):
        if self._html_data is not None:
            self._soup = BeautifulSoup(self._html_data, "html.parser")
        else:
            print("html data is none")
        return

    def find_tables_in_parsed_html_data(self):
        if self._soup is not None:
            self._tables = self._soup.find_all("table")
        else:
            print("beautiful soup is not initialized")
        return

    def find_rows_of_nth_table(self, n=-1):
        if self._tables is not None:
            self._table_rows = self._tables[n].find_all("tr")
        else:
            print("tables is none")
        return

    def find_table_with_id(self, table_id):
        if self._soup is not None:
            self._table = self._soup.find("table", id=table_id)
        else:
            print("beautiful soup is not initialized")
        return

    def find_rows_of_table(self):
        if self._table is not None:
            table_rows = []
            for row in self._table.find_all("tr"):
                row_values = []
                for col in row.find_all("td"):
                    row_values.append(col.get_text().strip())
                table_rows.append(row_values)
            self._table_rows = table_rows
        else:
            print("table is none")
        return

    def find_header_of_table(self):
        if self._table is not None:
            table_header = []
            for row_header in self._table.find_all("th"):
                table_header.append(row_header.get_text())
            self._table_header = table_header
        else:
            print("table is none")
        return
