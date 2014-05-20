import os
import sys
import glob
import getpass
import optparse, re


try:
    from mechanize import Browser
except ImportError:
    print "mechanize required but missing"
    sys.exit(1)

br = Browser()
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; \
	          rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	br.set_handle_robots(False)
	
def getBWAnchors( part ):
	return re.findall(r'>(.*?)<', part)	

def getResult(roll):

	# let browser fool robots.txt

	br.open('http://www.hpbose.org/Result/MatricResult.aspx')
	br.select_form(name="aspnetForm")
	br["ctl00$ContentPlaceHolder1$txtRollNo"] = roll 
	br.form.action = 'http://www.hpbose.org/Result/MatricResult.aspx'
	response = br.submit()

	result = response.read()
	return result

def writeToFile(result):
	write = open('result.html', 'w+')
	write.write(result)
	write.close()

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
for i in range(140659821, 140659922):
	result = getResult(str(i))
	writeToFile(result)
	print '[+] Got roll no. ' + str(i)
	print '[+] Writing it now'
	data = addData(data)
data += '</table>'

result = open('result.html', 'w+') 
result.write(data)
result.close()