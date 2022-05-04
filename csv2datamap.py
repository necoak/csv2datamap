import click
import codecs
import csv
from pprint import pprint
import shutil
import sys


def generate_row1_col1_map(csv_values, template_html_text, csv_column_index_for_row,
                            csv_column_index_for_column, csv_column_index_for_display):
    row_definitions = []
    for csv_value in csv_values:
        tmp_row_definition = csv_value[csv_column_index_for_row]
        if tmp_row_definition not in row_definitions:
            row_definitions.append(tmp_row_definition)

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

    html_printer = HtmlPrinter(template_html_text, 1)
    html_printer.add_table_header_column('#')
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


def is_match_kv2(key1, val1, key2, val2, kvlist):
    print(key1, val1, key2, val2, kvlist)
    is_ok1, is_ok2 = False, False
    for k, v in kvlist:
        if (k == key1) and (v == val1):
            is_ok1 = True
        if (k == key2) and (v == val2):
            is_ok2 = True
    if is_ok1 and is_ok2:
        return True
    else:
        return False


def generate_rown_col1(csv_kvlist, template_html_text,
                       rowname, columnname, displayname,
                       row_master, csv_column_definition):
    row_definitions = []
    keys = []
    with open(row_master, encoding='utf_8_sig') as row_master_csv_file:
        row_master_csv_reader = csv.reader(row_master_csv_file)
        _csv_records = []
        for csv_record in row_master_csv_reader:
            _csv_records.append(csv_record)

        row_definitions = convert_csv2kvlist(_csv_records)

    pprint(row_definitions)
    pprint('--------------------------')
    pprint(csv_kvlist)

    mymap = []
    for row_definition in row_definitions:
        ret_record = [row_definition]
        key = None
        pprint(row_definition)
        for k,v in row_definition:
            if k == rowname:
                key = v
        pprint(key)

        for column_key in csv_column_definition:
            print('column_key ', column_key)
            ret_record.append(
                list(filter(lambda kv: is_match_kv2(rowname, key, columnname, column_key, kv), csv_kvlist)))
        mymap.append(ret_record)
    pprint('--------------------------')
    pprint(mymap)

    html_printer = HtmlPrinter(template_html_text, len(row_definitions[0]))
    #
    for k,v in row_definitions[0]:
        pprint(k)
        html_printer.add_table_header_column(k)
    for column_key in csv_column_definition:
        pprint(column_key)
        html_printer.add_table_header_column(column_key)
    #
    for mymap_i in mymap:
        _record = []
        for k,v in mymap_i[0]:
            _record.append(v)
        for mymap_ij in mymap_i[1:]:
            target_elements = []
            for mymap_ijk in mymap_ij:
                for ijk_k, ijk_v in mymap_ijk:
                    if ijk_k == displayname:
                        target_elements.append(ijk_v)
            _record.append(target_elements)
        pprint('===========================')
        pprint(_record)
        html_printer.add_table_record(_record)

    html_printer.print()




def convert_csv2kvlist(csv_value):
    keys = csv_value[0]
    kvlist = []
    for record in csv_value[1:]:
        kvlist.append(list(zip(keys, record)))
    return kvlist


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

        _csv_records = []

        for row in csvreader:
            _csv_records.append(row)
            if len(csv_column_definitions) == 0:
                csv_column_definitions = row
            else:
                csv_values.append(row)

        csv_kvlist = convert_csv2kvlist(_csv_records)

        csv_column_index_for_row = csv_column_definitions.index(rowname)
        csv_column_index_for_column = csv_column_definitions.index(columnname)
        csv_column_index_for_display = csv_column_definitions.index(displayname)

        template_file = open('template/main_template.html', encoding="utf_8_sig")
        template_html_text = template_file.read()
        template_file.close()

        shutil.copy('template/style.css', 'out/style.css')

        # Column Definition
        column_definitions = []
        for csv_value in csv_values:
            tmp_column_definition = csv_value[csv_column_index_for_column]
            if tmp_column_definition not in column_definitions:
                column_definitions.append(tmp_column_definition)

        # Row Definition
        row_definitions = []
        if row_master is None:
            generate_row1_col1_map(csv_values, template_html_text, csv_column_index_for_row,
                                   csv_column_index_for_column, csv_column_index_for_display)
            sys.exit(0)

            for csv_value in csv_values:
                tmp_row_definition = csv_value[csv_column_index_for_row]
                if tmp_row_definition not in row_definitions:
                    row_definitions.append(tmp_row_definition)
        else:
            generate_rown_col1(csv_kvlist, template_html_text,
                               rowname, columnname, displayname,
                               row_master, column_definitions)
            sys.exit(9)
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
    def __init__(self, html_text, header_column_num):
        self.html_text = html_text
        self._table_headers = []
        self._table_records = []
        self._header_column_num = header_column_num

    def add_table_header_column(self, text):
        self._table_headers.append(text)

    def add_table_record(self, values):
        self._table_records.append(values)

    def print(self):
        table_headers = []
        table_bodies =  []

        for header in self._table_headers:
            table_headers.append('<th class="headline">%s</th>' % header)

        for record in self._table_records:
            # table_bodies.append('<tr>')
            for column_cell in record[:self._header_column_num]:
                table_bodies.append('<td class="headline">%s</td>' % column_cell)
            for column_cell in record[self._header_column_num:]:
                table_bodies.append('<td class="cell">')
                for column_cell_value in column_cell:
                    table_bodies.append('<div class="element">%s</div>' % column_cell_value)
                table_bodies.append('</td>')
            table_bodies.append('</tr>')

        html_text = self.html_text.\
            replace('<!---REPLACE1-->', '\n'.join(table_headers)).\
            replace('<!---REPLACE2-->', '\n'.join(table_bodies))
        print(html_text, file=codecs.open('./out/main.html', 'w', 'utf-8'))



if __name__ == "__main__":
    main()
