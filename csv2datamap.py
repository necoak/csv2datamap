import click
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


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.argument('rowname', type=click.STRING)
@click.argument('columnname', type=click.STRING)
@click.argument('displayname', type=click.STRING)
def main(filename, rowname, columnname, displayname):
    with open(filename, encoding='utf_8_sig') as csvfile:
        csvreader = csv.reader(csvfile)

        csv_column_definitions = []
        csv_values = []

        for row in csvreader:
            if len(csv_column_definitions) == 0:
                csv_column_definitions = row
            else:
                csv_values.append(row)

        csv_column_index_for_row = csv_column_definitions.index(rowname)
        csv_column_index_for_column = csv_column_definitions.index(columnname)
        csv_column_index_for_display = csv_column_definitions.index(displayname)

        # Row Definition
        row_definitions = []
        for csv_value in csv_values:
            tmp_row_definition = csv_value[csv_column_index_for_row]
            if tmp_row_definition not in row_definitions:
                row_definitions.append(tmp_row_definition)
        pprint(row_definitions)

        # Column Definition
        column_definitions = []
        for csv_value in csv_values:
            tmp_column_definition = csv_value[csv_column_index_for_column]
            if tmp_column_definition not in column_definitions:
                column_definitions.append(tmp_column_definition)
        pprint(column_definitions)

        # Row x Column で構造化
        for row_definition in row_definitions:
            for column_definition in column_definitions:
                print('%s %s : ' % (row_definition, column_definition), end='')
                targetvals = []
                for csv_value in csv_values:
                    if (csv_value[csv_column_index_for_row] == row_definition) and \
                            (csv_value[csv_column_index_for_column] == csv_column_index_for_column):
                        targetvals.append(csv_value)
                if len(targetvals) == 0:
                    print('None')
                else:
                    print(', '.join([v[4] for v in targetvals]))

        html_printer = HtmlPrinter()
        for column_definition in column_definitions:
            html_printer.add_table_header_column(column_definition)
        for row_definition in row_definitions:
            _record = []
            _record.append(row_definition)
            for column_definition in column_definitions:
                target_elements = []
                for csv_value in csv_values:
                    if ((csv_value[csv_column_index_for_row] == row_definition) and
                            (csv_value[csv_column_index_for_column] == column_definition)):
                        target_elements.append(csv_value[csv_column_index_for_display])
                _record.append(target_elements)
            html_printer.add_table_record(_record)

        html_printer.print()


class HtmlPrinter:
    def __init__(self):
        self._table_headers = []
        self._table_records = []

    def add_table_header_column(self, text):
        self._table_headers.append(text)

    def add_table_record(self, values):
        self._table_records.append(values)

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
