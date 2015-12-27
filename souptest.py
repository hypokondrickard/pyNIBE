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
    # get keys
    var_designations = [x.text for x in table.findAll('span', attrs={'class': 'VariableDesignation'})]

    # get values
    var_values = [x.text for x in table.findAll(attrs={'class': re.compile(r".*(AutoUpdateValue|ID0).*")})]

    # get descriptors
    var_descriptors = []
    table_body = table.find('tbody')
    for row in table_body.findAll('tr'):
        cols = [ele.contents[0].strip() for ele in row.findAll('td', limit=1)]
        var_descriptors.append(cols[0])

    # collapse result lists for this table
    this_table = zip(var_designations, var_values, var_descriptors)

    # populate result dict for this table
    table_name = all_table_names[table_id].text
    table_result = dict()
    for entry in this_table:
        table_result[entry[0]] = {'value': entry[1], 'decorator': entry[2]}

    result[table_name] = table_result

    table_id += 1

pprint(result)
