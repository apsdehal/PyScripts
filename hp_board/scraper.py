import optparse
import re
from bs4 import BeautifulSoup

import multiprocessing
from joblib import Parallel, delayed
import pickle

try:
    from mechanize import Browser
except ImportError:
    print "mechanize required but missing"
    sys.exit(1)

# Constants
WEBSITE = 'http://www.hpbose.org/Result/MatricResult.aspx'
ROLL_NO_HOLDER = "ctl00$ContentPlaceHolder1$txtRollNo"
FORM_NAME = "aspnetForm"

br = Browser()
# let browser fool robots.txt
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; \
          rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)


# Regex for getting data in between span anchors
def getBWAnchors(part):
    return re.findall(r'>(.*?)<', part)


# Get result of specific roll no and return the html response
def getResult(roll):
    try:
        br.open(WEBSITE)
        br.select_form(name=FORM_NAME)
        br[ROLL_NO_HOLDER] = str(roll)
        br.form.action = WEBSITE
        response = br.submit()

        result = response.read()

    except:
        return getResult(roll)
    print '[+] Got roll no. ' + str(roll)
    return result


# Just a regular workaround for getting data as I need
def writeToFile(result):
    write = open('result.html', 'w+')
    write.write(result)
    write.close()

CLASS_HOLDER = "ctl00_ContentPlaceHolder1%s"

# Now add data to the data variable already created
def parseAndAdd(data, result):
    soup = BeautifulSoup(result, "html5lib")
    # try:
    result = {}
    result_div = soup.find(id=CLASS_HOLDER % "_pnlresult")
    result_tbody = result_div.find("table").findAll("tbody")[1]
    trs = result_tbody.findAll("tr")
    name = result_div.find(id=CLASS_HOLDER % "_lblStudentName").getText()
    result["name"] = name.encode("ascii", "ignore")
    rollno = result_div.find(id=CLASS_HOLDER % "_lblRollNo").getText()
    result["rollno"] = rollno.encode("ascii", "ignore")

    for i in range(0, 8):
        subject = result_div.find(id=CLASS_HOLDER % "_lblSub" + str(i))
        marks = result_div.find(id=CLASS_HOLDER % "_lblres" + str(i))

        if subject != None and marks != None:
            subject = subject.getText()
            marks = marks.getText()
            result[subject.strip().lower().encode("ascii", "ignore")] = marks.strip().lower().encode("ascii", "ignore")

    result["result"] = result_div.find(id=CLASS_HOLDER % "_lblResult").getText().encode("ascii", "ignore")
    print(result)
    data = addResult(data, result)
    # except:
    #     pass
    return data

average = {}
def addResult(data, result):
    data += '<tr>'
    for sub in ["rollno", "name", "english", "mathematics", "hindi", "social science", "science", "sanskrit", "art", "computer science", "result"]:
        answer = result.get(sub, "")
        data += '<td>' + answer + '</td>'
        if sub != "rollno" and sub != "name" and sub != "result":
            if sub not in average:
                average[sub] = []
            if len(answer) and answer != "c" and answer != "f":
                average[sub].append(float(answer.replace("*", "")))

    data += '</tr>'
    return data


# Get initial data with table tags
def getInitialData():
    data = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Results 2017</title><style> table {text-align: center;border-collapse: collapse;} th {font-weight: bold;}th, td {padding: 0px 5px;border: 1px solid #000;}</style></head><body>'
    data += '<table>'
    data += '<tr>'
    data += '<th>Rollno</th>'
    data += '<th>Name</th>'
    data += '<th>English</th>'
    data += '<th>Math</th>'
    data += '<th>Hindi</th>'
    data += '<th>SST</th>'
    data += '<th>Science</th>'
    data += '<th>Sanskrit</th>'
    data += '<th>Art</th>'
    data += '<th>Computer Science</th>'
    data += '<th>Result</th>'
    data += '</tr>'
    return data

def getAverage(data):
    data += "<tr><td>Average</td><td></td>"

    for sub in ["english", "mathematics", "hindi", "social science", "science", "sanskrit", "art", "computer science"]:
        data += "<td>" + str(round(sum(average[sub]) / len(average[sub]), 3)) + "</td>"

    data += "</tr>"

    return data


if __name__ == '__main__':
    data = getInitialData()
    num_cores = multiprocessing.cpu_count()
    results = Parallel(n_jobs=num_cores)(delayed(getResult)(str(i)) for i in range(1714547001, 1714547077))
    # Be safe just in case
    pickle.dump(results, open("results", "wb"))
    results = pickle.loads(open("results", "rb").read())
    print '[+] Writing it now'
    print(len(results))
    for result in results:
        data = parseAndAdd(data, result)

    data = getAverage(data)
    data += '</table></body></html>'
    result = open('result2.html', 'w+')
    result.write(data)
    result.close()

'''
Write the result to file
'''
