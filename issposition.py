#import urllib2
import urllib.request as urllib2
import json
import time
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


req = urllib2.Request("http://api.open-notify.org/iss-now.json")
response = urllib2.urlopen(req)

obj = json.loads(response.read())

while(True):
	plt.figure(1)
	map = Basemap(projection='cyl',resolution='i')
	x, y = map(obj['iss_position']['longitude'], obj['iss_position']['latitude'])
	map.plot(x, y, 'o', markersize=5,color='red',alpha=1) 
	map.etopo()
	map.drawcoastlines(color='black')
	#plt.show()
	plt.savefig('img{:02d}.png'.format(int(obj['timestamp'])),bbox_inches='tight',dpi=96)
	time.sleep(1)
#map.drawcountries(color='black')
#time.sleep(1)