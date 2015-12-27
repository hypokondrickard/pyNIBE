import requests

class pyNIBE(object):

    def __init__(self, username, password):
        """

        """
        self.username = username
        self.password = password
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
        r = requests.get('https://www.nibeuplink.com/System/21264/Status/ServiceInfo', cookies=self.session.cookies.get_dict())
        self.readings = r.content

    def open(self):
        self._login()
        self._get()
