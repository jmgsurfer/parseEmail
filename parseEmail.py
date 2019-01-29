from BeautifulSoup import BeautifulSoup # pip install beautifulsoup
import urllib2 # Body analyze for href and title
import email.parser
import sys
import re
#
receivedFrom = {}
tmpIp = ''
#
with open(sys.argv[1], 'r') as myMail:
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
print  
#
print "====================="
print "Message Body analysis"
print "====================="
msg_html = urllib2.urlopen("file:///home/matrixx/hubic/scripts/confirmation.eml")
soup = BeautifulSoup(msg_html)
for link in soup.findAll('a'):
    if link.string <> None:
        print "<",link.string,">"
        print "   Initial Link:", link.get('href')
        # Below to be run with Tor
        #req =urllib2.Request(link.get('href'))
        #res =urllib2.urlopen(req)
        #print "Final Link:", res.geturl()



