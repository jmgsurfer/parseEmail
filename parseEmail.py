from bs4 import BeautifulSoup # pip install beautifulsoup4
import urllib2 # Body analyze for href and title
import email.parser
import sys
import re
import os
#
file = sys.argv[1]
#path_file = os.path.split(file)[0]
receivedFrom = {}
tmpIp = ''
#
os.system('clear||cls')
#
if os.path.split(file)[0] == "":
    file = os.getcwd() + "/" + file

if not os.path.exists(file):
    print "Argument file does not exist! \nExiting ...!"
    exit()
#
with open(file, 'r') as myMail:
    msg = email.parser.Parser().parse(myMail, True)

for k,v in msg.items():
    try:
        tmpIp = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', v).group()
    except:
        tmpIp = ''
    if k == 'Received':
        temp = v.split()
        idx_by = temp.index('by')
        receivedFrom["Received"] = temp[1]
        receivedFrom["IP"] = tmpIp
        receivedFrom["Date"] = v.split(';')[1]
        receivedFrom["By"] = temp[idx_by + 1]
print "======================="
print "Message Header analysis"
print "======================="
print "Message-ID:", msg.get('Message-ID')
print "Reply-To:", msg.get('Reply-To')
print "Return-Path:", msg.get('Return-Path')
print "To:", msg.get('To')
print "===" 
print "Subject:", msg.get('Subject') 
print "===" 
print "1st Received:", "from", receivedFrom.get('Received'), "IP:", receivedFrom.get('IP')
print "by:", receivedFrom.get('By')
print "on:", receivedFrom.get('Date')
#
print "\n====================="
print "Message Body analysis"
print "====================="
msg_html = urllib2.urlopen("file://" + file)
soup = BeautifulSoup(msg_html,'lxml')

print "Page link retrieval:"
print "--------------------"
for link in soup.find_all('a'):
    if link.string <> None:
        print "<",link.string,">"
        print "   Initial Link:", link.get('href')
        # Below to be run with Tor
        #req =urllib2.Request(link.get('href'))
        #res =urllib2.urlopen(req)
        #print "Final Link:", res.geturl()
print "\nImage link retrieval:"
print "----------------------"
for link2 in soup.find_all('img'):
    if link2.get('src') <> "":
        print link2.get('src')
