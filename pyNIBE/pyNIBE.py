from BeautifulSoup import BeautifulSoup
import requests
import re


class pyNIBE(object):
    def __init__(self, username, password, system_id):
        """
        in order to extract information from our NIBE heat pump, we need to provide the following
        username: credentials for our user NIBE UPLINK service 
        password: credentials for our user NIBE UPLINK service 
        system_id: the ID for the heat pump we're interested in. 
            This can be found in the URL after having logged in to the webui of the NIBE UPLINK service.
            for example, https://www.nibeuplink.com/System/12345/Status/Overview would reveal a system_id of '12345'.
        """
        self.username = username
        self.password = password
        self.system_id = system_id
        self.session = None

    def _login(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        data = 'returnUrl=&Email=%s&Password=%s' % (self.username, self.password)

        self.session = requests.Session()

        self.session.post('https://www.nibeuplink.com/LogIn', headers=headers, data=data)

    def _logout(self):
        requests.get('https://www.nibeuplink.com/LogOut', cookies=self.session.cookies.get_dict())

    def _get(self):
        r = requests.get('https://www.nibeuplink.com/System/%s/Status/ServiceInfo' % self.system_id,
                         cookies=self.session.cookies.get_dict())

        soup = BeautifulSoup(r.content)

        all_table_names = soup.findAll('h3')
        all_tables = soup.findAll('table', {"class": 'Sortable {sortlist: [[0,0]]}'})

        result = dict()

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
            table_name = all_table_names.pop(0).text

            table_result = dict()

            num_sensors = len(this_table)

            i = 0
            for entry in this_table:
                table_result[i] = {'sensor-code': entry[0], 'value': entry[1], 'descriptor': entry[2]}
                i += 1

            result[table_name] = table_result

        self.readings = result

    def open(self):
        if not self.session:
            self._login()
            self._get()
        else:
            pass

    def close(self):
        if self.session:
            self._logout()
            self.readings = None
            self.session = None
        else:
            pass

    def refresh(self):
        if self.session:
            self._get()
        else:
            pass
