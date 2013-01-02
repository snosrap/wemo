from miranda import upnp, msearch

conn = upnp(False,False,None,[])

class WeMo(object):
	hostName = None
	controlURL = None

	def __init__(self, hostInfo={}, controlURL=None):
		if hostInfo:
			self.hostName = hostInfo['name']
			self.controlURL = '%s%s%s' % (hostInfo['proto'], hostInfo['name'], hostInfo['deviceList']['controllee']['services']['basicevent']['controlURL'])
		elif controlURL:
			self.hostName = controlURL.split('/')[2] # TODO: urlparse
			self.controlURL = controlURL

	def __str__(self):
		return self.friendlyName

	def send(self, action, args={}):
		resp = conn.sendSOAP(self.hostName, 'urn:Belkin:service:basicevent:1', self.controlURL, action, args)
		if conn.extractSingleTag(resp, "UPnPError"):
			raise Exception(resp)
		return resp

	@property
	def friendlyName(self):
		return conn.extractSingleTag(self.send('GetFriendlyName'), 'FriendlyName')
	
	@friendlyName.setter
	def friendlyName(self, value):
		self.send('ChangeFriendlyName', {'FriendlyName': (value, 'String')})

	@property
	def binaryState(self):
		return conn.extractSingleTag(self.send('GetBinaryState'), 'BinaryState') in ['1']

	@binaryState.setter
	def binaryState(self, value):
		self.send('SetBinaryState', {'BinaryState': (int(value), 'Boolean')})

	@property
	def iconURL(self):
		return conn.extractSingleTag(self.send('GetIconURL'), 'URL')

	@property
	def logFileURL(self):
		return conn.extractSingleTag(self.send('GetLogFileURL'), 'LOGURL')

def search():
	conn.TIMEOUT = 2
	conn.UNIQ = True
	msearch(0, 0, conn)

	wemos = []
	for index, hostInfo in conn.ENUM_HOSTS.iteritems():
		if hostInfo['dataComplete'] == False:
			xmlHeaders, xmlData = conn.getXML(hostInfo['xmlFile'])
			conn.getHostInfo(xmlData, xmlHeaders, index)
		try:
			if conn.ENUM_HOSTS[index]['deviceList']['controllee']['modelName'] == 'Socket':
				wemos.append(WeMo(hostInfo))
		except Exception, e:
			pass
	return wemos

if __name__ == "__main__":
	wemos = search()
	for wemo in wemos:
		print wemo.binaryState, wemo.friendlyName