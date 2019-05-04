from bs4 import BeautifulSoup # pip install beautifulsoup4
import whois # pip install python-whois
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
domainList = []
enc = 'none'
#
def is_windows():
    if os.name == 'nt':
        return True
    else:
        return False
#
def domain(url):
    d = re.search('(www\.|\:\/\/)+([\w\-\.]+)', url)
    return d.group(len(d.groups()))
#
def isPresent(elt, lst):
    return elt in lst

def appendToListe(element, liste):
    liste.append(element)
    return
#
os.system('clear||cls')
#
if os.path.split(file)[0] == "":
    if is_windows():
        file = os.getcwd() + "\\" + file
        url_file = "/" + file.replace("\\","/")
        print "window: ", file
        print url_file
    else:    
        file = os.getcwd() + "/" + file
        url_file = file
        print file

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
        receivedFrom["Received"] = temp[1]
        receivedFrom["IP"] = tmpIp
        receivedFrom["Date"] = v.split(';')[1]
        receivedFrom["By"] = v.split('\n')[1].split()[1]
    if k == 'Content-Transfer-Encoding':
        enc = v
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
print "==="
print "Content-Transfer-encoding:", enc
#
print "\n====================="
print "Message Body analysis"
print "====================="
msg_html = urllib2.urlopen("file://" + url_file)
if is_windows():
    soup = BeautifulSoup(msg_html, features="html.parser")
else:
    soup = BeautifulSoup(msg_html, 'lxml')

print "Page link retrieval:"
print "--------------------"
for link in soup.find_all('a'):
    if link.string <> None:
        print "<",link.string,">"
        print "   Initial Link:", link.get('href')
        if not isPresent(domain(link.get('href')),domainList):
            appendToListe(domain(link.get('href')),domainList)

        # Below to be run with Tor
        #req =urllib2.Request(link.get('href'))
        #res =urllib2.urlopen(req)
        #print "Final Link:", res.geturl()
print "\nImage link retrieval:"
print "----------------------"
for link2 in soup.find_all('img'):
    if link2.get('src') <> "":
        print link2.get('src')
        if not isPresent(domain(link2.get('src')),domainList):        
            appendToListe(domain(link2.get('src')),domainList)
#print domainList
print "\nDomain Whois Information:"
print "--------------------------"
for d in domainList:
    try:
        w = whois.whois(d)
        print d, "-> creation date: ", str(w.creation_date)
        print "--"
    except:
        print d, "was deleted. No more Whois information available."
        

