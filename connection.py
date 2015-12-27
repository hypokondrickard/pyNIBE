import requests
from BeautifulSoup import BeautifulSoup
import sys

def getCookie(username,password):
	cookies = {
	    'BIGipServerUplink_www_pool': '1695000768.20480.0000',
	    'EmilLanguage': 'en-US',
	    '__utmt': '1',
	    '__utma': '18108838.998944294.1444745470.1444745470.1444745470.1',
	    '__utmb': '18108838.51.10.1444745470',
	    '__utmc': '18108838',
	    '__utmz': '18108838.1444745470.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
	}

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

	data = 'returnUrl=&Email=%s&Password=%s' % (username,password)


	session = requests.Session()

	session.post('https://www.nibeuplink.com/LogIn', headers=headers, cookies=cookies, data=data)

	return session.cookies.get_dict()

username = sys.argv[1]
password = sys.argv[2]

#r = requests.get('https://www.nibeuplink.com/System/21264/Status/ServiceInfo', cookies=getCookie(username, password))
r = requests.get('https://www.nibeuplink.com/', cookies=getCookie(username, password))
print r.content
