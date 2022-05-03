import click
import codecs
import csv
from pprint import pprint
import shutil


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.argument('rowname', type=click.STRING)
@click.argument('columnname', type=click.STRING)
@click.argument('displayname', type=click.STRING)
@click.option('--row_master', type=click.Path(exists=True))
@click.option('--column_master', type=click.Path(exists=True))
def main(filename, rowname, columnname, displayname,
         row_master, column_master):

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

        template_file = open('template/main_template.html', encoding="utf_8_sig")
        template_html_text = template_file.read()
        template_file.close()

        shutil.copy('template/style.css', 'out/style.css')

        # Row Definition
        row_definitions = []
        if row_master is None:
            for csv_value in csv_values:
                tmp_row_definition = csv_value[csv_column_index_for_row]
                if tmp_row_definition not in row_definitions:
                    row_definitions.append(tmp_row_definition)
        else:
            with open(row_master,   encoding='utf_8_sig') as row_master_csv_file:
                row_master_csv_reader = csv.reader(row_master_csv_file)
                for row_master in row_master_csv_reader:
                    row_definitions.append(row_master[0])
                row_definitions = row_definitions[1:]


        # Column Definition
        column_definitions = []
        for csv_value in csv_values:
            tmp_column_definition = csv_value[csv_column_index_for_column]
            if tmp_column_definition not in column_definitions:
                column_definitions.append(tmp_column_definition)

        # Row x Column で構造化
        for row_definition in row_definitions:
            for column_definition in column_definitions:
                targetvals = []
                for csv_value in csv_values:
                    if (csv_value[csv_column_index_for_row] == row_definition) and \
                            (csv_value[csv_column_index_for_column] == csv_column_index_for_column):
                        targetvals.append(csv_value)

        html_printer = HtmlPrinter(template_html_text)
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
    def __init__(self, html_text):
        self.html_text = html_text
        self._table_headers = []
        self._table_records = []

    def add_table_header_column(self, text):
        self._table_headers.append(text)

    def add_table_record(self, values):
        self._table_records.append(values)

    def print(self):
        table_headers = []
        table_bodies =  []

        for header in self._table_headers:
            table_headers.append('<th>%s</th>' % header)

        for record in self._table_records:
            table_bodies.append('<tr>')
            table_bodies.append('<td>%s</td>' % record[0])
            for column_cell in record[1:]:
                table_bodies.append('<td>')
                for column_cell_value in column_cell:
                    table_bodies.append('<div>%s</div>' % column_cell_value)
                table_bodies.append('</td>')
            table_bodies.append('</tr>')

        html_text = self.html_text.\
            replace('<!---REPLACE1-->', '\n'.join(table_headers)).\
            replace('<!---REPLACE2-->', '\n'.join(table_bodies))
        print(html_text, file=codecs.open('./out/main.html', 'w', 'utf-8'))



if __name__ == "__main__":
    main()
