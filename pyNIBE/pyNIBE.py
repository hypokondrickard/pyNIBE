from BeautifulSoup import BeautifulSoup
import requests
import re

class pyNIBE(object):

    def __init__(self, username, password, system_id):
        """

        """
        self.username = username
        self.password = password
        self.system_id = system_id
        self.session = None

    def _login(self):
        headers = {
            'Origin': 'https://www.nibeuplink.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.nibeuplink.com/Welcome',
            'Connection': 'keep-alive',
        }

        data = 'returnUrl=&Email=%s&Password=%s' % (self.username,self.password)

        self.session = requests.Session()

        self.session.post('https://www.nibeuplink.com/LogIn', headers=headers, data=data)

    def _get(self):
        r = requests.get('https://www.nibeuplink.com/System/%s/Status/ServiceInfo' % self.system_id, cookies=self.session.cookies.get_dict())

        soup = BeautifulSoup(r.content)

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
                table_result[entry[0]] = {'value': entry[1], 'descriptor': entry[2]}

            result[table_name] = table_result

            table_id += 1

        self.readings = result

    def open(self):
        self._login()
        self._get()
