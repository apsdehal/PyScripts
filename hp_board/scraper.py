import optparse, re

try:
    from mechanize import Browser
except ImportError:
    print "mechanize required but missing"
    sys.exit(1)

#Constants
WEBSITE = 'http://www.hpbose.org/Result/MatricResult.aspx'
ROLL_NO_HOLDER = "ctl00$ContentPlaceHolder1$txtRollNo"
FORM_NAME = "aspnetForm"

br = Browser()
# let browser fool robots.txt
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; \
          rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)

'''
Regex for getting data in between span anchors
'''	
def getBWAnchors( part ):
	return re.findall(r'>(.*?)<', part)	

'''
Get result of specific roll no and return the html response
'''
def getResult(roll):
	br.open(WEBSITE)
	br.select_form(name=FORM_NAME)
	br[ROLL_NO_HOLDER] = roll 
	br.form.action = WEBSITE
	response = br.submit()

	result = response.read()
	return result

'''
Just a regular workaround for getting data as I need
'''
def writeToFile(result):
	write = open('result.html', 'w+')
	write.write(result)
	write.close()

'''
Now add data to the data variable already created
'''
def addData(data):
	lines = open('result.html', 'r')
	lines = lines.readlines()
	try:
		name = getBWAnchors(lines[321])[0]
		rollno = getBWAnchors(lines[327])[0]
		english = getBWAnchors(lines[396])[0]
		math = getBWAnchors(lines[417])[0]
		hindi = getBWAnchors(lines[432])[0]
		sst = getBWAnchors(lines[447])[0]
		science = getBWAnchors(lines[468])[0]
		sanskrit = getBWAnchors(lines[477])[0]
		art = getBWAnchors(lines[498])[0]
		result = getBWAnchors(lines[408])[0]
		data += '<tr>'
		data += '<td>'+ rollno + '</td>'
		data += '<td>'+ name +'</td>'
		data += '<td>'+ english +'</td>'
		data += '<td>'+ math +'</td>'
		data += '<td>'+ hindi +'</td>'
		data += '<td>'+ sst +'</td>'
		data += '<td>'+ science +'</td>'
		data += '<td>'+ sanskrit +'</td>'
		data += '<td>'+ art +'</td>'
		data += '<td>'+ result +'</td>'
		data += '</tr>'
	except:
		pass	
	return data

'''
Get initial data with table tags
'''
def getInitialData():
	data = '<table>'
	data += '<tr>'
	data += '<th>Rollno</th>'
	data += '<th>Name</th>'
	data += '<th>English</th>'
	data += '<th>Math</th>'
	data += '<th>Hindi</th>'
	data += '<th>SST</th>'
	data += '<th>Science</th>'
	data += '<th>Sanskrit</th>'
	data += '<th>Art/Comp</th>'
	data += '<th>Result</th>'
	data += '</tr>'
	return data

data = getInitialData()
for i in range(140659821, 140659922):
	result = getResult(str(i))
	writeToFile(result)
	print '[+] Got roll no. ' + str(i)
	print '[+] Writing it now'
	data = addData(data)
data += '</table>'

'''
Write the result to file
'''
result = open('result.html', 'w+') 
result.write(data)
result.close()