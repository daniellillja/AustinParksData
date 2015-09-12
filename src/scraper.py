import lxml.html
import csv

class ParkRow:
	def __init__(self, rowElement):
		cols = rowElement.findall('td')
		
		self.nameCol = cols[0]
		self.addrCol = cols[1]
		self.serviceDistCol = cols[2]
		self.distMgrCol = cols[3]
		self.acresCol = cols[4]

	def isvalid(self):
		return len(self.nameCol.text.strip('\n').strip('\t')) > 5

class Park:
	def __init__(self, parkRow):
		self.name = self.formatstring(parkRow.nameCol.text)
		self.address = self.formatstring(parkRow.addrCol.text)
		self.district = self.formatstring(parkRow.serviceDistCol.text)
		self.manager = self.formatstring(parkRow.distMgrCol.text)
		self.acres = self.formatstring(parkRow.acresCol.text)

		self.csvrow = [self.name, self.address, self.district, self.manager, self.acres]

	def formatstring(self, string):
		return string.strip('\n').strip('\t').encode('ascii', 'ignore')



parkUrl = 'http://www.austintexas.gov/page/park-directory'

doc = lxml.html.parse(parkUrl)

rowElements = doc.xpath('//*[@id="node-11426"]/div/div[1]/div/div/table/tbody[2]/tr')
parkRows = []
for el in rowElements:
	row = ParkRow(el)
	if row.isvalid():
		parkRows.append(row)

parks = []
for parkRow in parkRows:
	parks.append(Park(parkRow))


for park in parks:
	print(repr(park.name))


outputfile='../results/parks.csv'

with open(outputfile, 'wb') as csvfile:
	spamwriter = csv.writer(csvfile)
	for park in parks:
		spamwriter.writerow(park.csvrow)
	
