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




if __name__ == "__main__":
    main()
