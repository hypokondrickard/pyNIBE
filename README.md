pyNIBE
=====

python module for retreival of measurement data from the NIBE UPLINK service

Installation
============

To install, clone this repo and execute:

```
python setup.py install
```

Documentation
=============
Please note that this is a web scraping library. User experience may vary.

this module will present the user with a dict of dicts holding all values presented in the Service Info-view of the NIBE Uplink webUI. 

[sample output](tests/mock-data/sample-output.txt)

Also, all values retrieved from NIBE UPLINK are preserved in the way they were retrieved, namely as unicode strings. This means that for whatever application you have, you will need to convert the readouts into a more suiting forms.

Before we proceed, we need to find the system ID of the heater we're interested in. The easiest way to get this is to log in to the nibe uplink webservice and click the system you're interested in. At this point, looking at the adress field of your web browser, you should see something like: https://www.nibeuplink.com/System/12345/Status/Overview, where 12345 is your system ID.

Examples
========

### Connect

Connect to the NIBE uplink service:
```python
>>> from pyNIBE import pyNIBE
>>> my_heater = pyNIBE('<nibe uplink username>','<nibe uplink password>','<system ID>')
>>> my_heater.open()
>>> outdoor_temperature = my_heater.readings['status'][0]['value']
>>> my_heater.close()
```

### Refresh measurement data
```python
>>> while True:
>>>    my_heater.refresh()
>>>    print my_heater.readings
>>>    time.sleep(5)
```

### Ship data to influxDB
```python
from pyNIBE import pyNIBE
from influxdb import InfluxDBClient
import json
import time

client = InfluxDBClient('<hostname>', <port>, '<username>', '<password>', '<database>')

my_heater = pyNIBE('<nibe uplink username>','<nibe uplink password>','<system ID>')
my_heater.open()

while True:
	# first value of the 'status'-section holds "BT1 Outdoor temperature"
	outdoor_temperature = my_heater.readings['status'][0]['value']

	# an awful way of killing the centigrade unit and converting to float
	outdoor_temperature = float(outdoor_temperature[0:-2])

	# bagging and tagging our data
	my_datapoint["measurement"] = "NIBE-1245-8"
	my_datapoint["tags"] = {'sensor': 'outdoor'}
	my_datapoint["fields"] = {'value': outdoor_temperature}

	# sending our data to influxDB
	client.write_points([my_datapoint])

	# wait for a while and start over
	time.sleep(300)
```

Thanks
======
Thanks to NIBE for lending me some gear to facilitate my home automation ventures.
