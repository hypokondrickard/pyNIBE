from BeautifulSoup import BeautifulSoup
import re
from pprint import pprint

ecj_data = open("mock-overview", 'r').read()

soup = BeautifulSoup(ecj_data)

all_table_names = soup.findAll('h3')
all_tables = soup.findAll('table', {"class": 'Sortable {sortlist: [[0,0]]}'})

result = dict()

table_id = 0
for table in all_tables:

    var_designation_elems = table.findAll('span', attrs={'class': 'VariableDesignation'})
    var_value_elems = table.findAll(attrs={'class': re.compile(r".*(AutoUpdateValue|ID0).*")})

    var_designations = [x.text for x in var_designation_elems]
    var_values = [x.text for x in var_value_elems]

    var_decorators = []
    table_body = table.find('tbody')
    for row in table_body.findAll('tr'):
        cols = row.findAll('td', limit=1)
        cols = [ele.contents[0].strip() for ele in cols]
        var_decorators.append(cols[0])

    this_table = zip(var_designations, var_values, var_decorators)

    table_name = all_table_names[table_id].text
    table_result = dict()
    for entry in this_table:
        table_result[entry[0]] = {'value': entry[1], 'decorator': entry[2]}

    result[table_name] = table_result

    table_id += 1

pprint(result['status']['BT1']['value'])
