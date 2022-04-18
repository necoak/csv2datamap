import codecs
import csv
from pprint import pprint


class ColumnDefinitions:
    def __init__(self):
        self.colum_definitions = []

    def add(self, column_name):
        self.colum_definitions.append(ColumnDefinition(column_name))


class ColumnDefinition:
    def __init__(self, column_name):
        self.column_name = column_name


class HtmlPrinter:
    pass


def main():
    with open('sample/baseball2020ja.csv', encoding='utf_8_sig') as csvfile:
        csvreader = csv.reader(csvfile)

        column_definitions = []
        values = []

        for row in csvreader:
            if len(column_definitions) == 0:
                column_definitions = row
            else:
                values.append(row)

        print('球団マスタ')
        teams = []
        for value in values:
            team = value[0]
            if team not in teams:
                teams.append(team)
        pprint(teams)

        print('ポジションマスタ')
        positions = []
        for value in values:
            position = value[1]
            if position not in positions:
                positions.append(position)
        pprint(positions)

        for team in teams:
            for position in positions:
                print('%s %s : ' % (team, position), end='')
                targetvals = []
                for value in values:
                    if (value[0] == team) and (value[1] == position):
                        targetvals.append(value)
                if len(targetvals) == 0:
                    print('None')
                else:
                    print(', '.join([v[4] for v in targetvals]))

        html_printer = HtmlPrinter()
        for position in positions:
            html_printer.add_table_header_column(position)
        for team in teams:
            _record = []
            _record.append(team)
            for position in positions:
                target_players = []
                for value in values:
                    if (value[0] == team) and (value[1] == position):
                        target_players.append(value[4])
                _record.append(target_players)
            html_printer.add_table_record(_record)

        html_printer.print()



class HtmlPrinter:
    def __init__(self):
        self.content = []
        self._table_headers = []
        self._table_records = []

    def setup(self):
        self.add('''
            <!DOCTYPE html>
                <html lang="ja">
                <head>
                    <meta charset="UTF-8">
                    <title>出力例</title>
                    <style type="text/css">
                        table, td {
                            border: solid;
                        }
                    table tr td:nth-of-type(1){
                        background-color: #333;
                        color: #fff;
                    }
                    thead, tfoot {
                        background-color: #333;
                        color: #fff;
                    }
                    div {
                        background-color: #BAD3FF;
                        margin : 10px;
                        }
                    </style>
                </head>
            ''')

    def setDown(self):
        self.add('''
                </body>
            </html>
        ''')

    def start_body(self):
        self.add('<body>')

    def close_body(self):
        self.add('</body>')

    def start_table(self):
        self.add('<table>')

    def close_table(self):
        self.add('</table>')

    def start_table_header(self):
        self.add('''
            <thead>
                <tr>
            ''')
        self.add_table_header_column('#')

    def add_table_header_column(self, text):
        self._table_headers.append(text)

    def add_table_record(self, values):
        self._table_records.append(values)

#    def add_table_header_column(self, text):
#        self.add('<th>%s</th>' % text)

    def close_table_header(self):
        self.add('''
                </tr>
            </thead>
            ''')

    def start_table_body(self):
        self.add('<tbody>')

    def start_table_record(self, text):
        self.add('<tr>')
        self.add('<td>%s</td>' % text)

    def add_table_body_cell(self, values):
        self.add('<td>')
        for value in values:
            self.add('<div>%s</div>' % value)
        self.add('</td>')

    def close_table_record(self):
        self.add('</tr>')

    def add(self, text):
        self.content.append(text)

    def print(self):
        content = []
        content.append('''\
            <!DOCTYPE html>
                <html lang="ja">
                <head>
                    <meta charset="UTF-8">
                    <title>出力例</title>
                    <style type="text/css">
                        table, td {
                            border: solid;
                        }
                    table tr td:nth-of-type(1){
                        background-color: #333;
                        color: #fff;
                    }
                    thead, tfoot {
                        background-color: #333;
                        color: #fff;
                    }
                    div {
                        background-color: #BAD3FF;
                        margin : 10px;
                        }
                    </style>
                </head>
                ''')
        content.append('<body>')
        content.append('<table>')
        content.append('<thead>')
        content.append('<tr>')
        content.append('<th>#</th>')
        for header in self._table_headers:
            content.append('<th>%s</th>' % header)
        content.append('</tr>')
        content.append('</thead>')
        content.append('<tbody>')
        for record in self._table_records:
            content.append('<tr>')
            content.append('<td>%s</td>' % record[0])
            for column_cell in record[1:]:
                content.append('<td>')
                for column_cell_value in column_cell:
                    content.append('<div>%s</div>' % column_cell_value)
                content.append('</td>')
            content.append('</tr>')
        content.append('</table>')
        content.append('</body>')
        print('\n'.join(content), file=codecs.open('out.html', 'w', 'utf-8'))


if __name__ == "__main__":
    main()
