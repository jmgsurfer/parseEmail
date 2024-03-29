from bs4 import BeautifulSoup # used to scrape html part of email
import whois # used to retrieve info from url found in email
import email.parser # used to parse headers, body from email
import sys # used to get argument (email file)
import re # used to catch IP address
import os
import base64
import quopri
#
# To ensure all necessary modules are installed: pip install -r requirements.txt
#
# manage argument passed in command line: python parsEmail.py emailFileToBeProcessed.eml
try:
    file = sys.argv[1]
except:
    print("No argument (file name) specified. \nExiting ...!")
    exit()
#path_file = os.path.split(file)[0]
receivedFrom = {} # dictionary for received header split contents
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
#
def appendToListe(element, liste):
    liste.append(element)
    return
#
def bodyDecode64(beml):
    return
#
os.system('clear||cls') # start by clear the terminal
# Below will be used when path of file specified in argument is not in current working directory.
#if os.path.split(file)[0] == "":
#    if is_windows():
#        file = os.getcwd() + "\\" + file
#        url_file = "/" + file.replace("\\","/")
#        print("window: ", file)
#        print(url_file)
#    else:    
#        file = os.getcwd() + "/" + file
#        url_file = file
#        print(file)
#if not os.path.exists(file):
#    print("Argument file does not exist! \nExiting ...!")
#    exit()
# Above will be used when path of file specified in argument is not in current working directory.

with open(file, 'r') as myMail:
    msg = email.parser.Parser().parse(myMail) # use to parse myMail email file for header only (True)

msg_html = msg.get_payload() # get email body only

for k,v in msg.items():
    try:
        tmpIp = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', v).group()
    except:
        tmpIp = ''
    if k == 'Received':
        try:
            temp = v.split()
            receivedFrom["Received"] = temp[1]
            receivedFrom["IP"] = tmpIp
            receivedFrom["Date"] = v.split(';')[1]
            receivedFrom["By"] = v.split('\n')[1].split()[1]
        except:
           None
    if k == 'Content-Transfer-Encoding':
        enc = v
        if enc == "base64":
            msg_html = base64.decodestring(msg_html)
        if enc == "quoted-printable":
            msg_html = quopri.decodestring(msg_html)
#
print("=======================")
print("Message Header analysis")
print("=======================")
print("Message-ID:", msg.get('Message-ID'))
print("Reply-To:", msg.get('Reply-To'))
print("Return-Path:", msg.get('Return-Path'))
print("To:", msg.get('To'))
print("===")
print("Subject:", msg.get('Subject')) 
print("===")
print("1st Received:", "from", receivedFrom.get('Received'), "IP:", receivedFrom.get('IP'))
print("by:", receivedFrom.get('By'))
print("on:", receivedFrom.get('Date'))
print("===")
print("Content-Transfer-encoding:", enc)
print("\n=====================")
print("Message Body analysis")
print("=====================")

#if is_windows():
#    soup = BeautifulSoup(msg_html, features="html.parser")
#else:
with open(file, "r") as myFile:
    soup = BeautifulSoup(myFile, 'lxml')

print("Page link retrieval:")
print("--------------------")
for link in soup.find_all('a'):
    if link.string != None:
        print("<",link.string,">")
        print("   Initial Link:", link.get('href'))
        if not isPresent(domain(link.get('href')),domainList):
            appendToListe(domain(link.get('href')),domainList)


print("\nImage link retrieval:")
print("----------------------")
for link2 in soup.find_all('img'):
    if link2.get('src') != "":
        print(link2.get('src'))
        if not isPresent(domain(link2.get('src')),domainList):        
            appendToListe(domain(link2.get('src')),domainList)

print("\nDomain Whois Information:")
print("--------------------------")
for d in domainList:
    try:
        w = whois.whois(d)
        print(d, "-> creation date: ", str(w.creation_date))
        print("--")
    except:
        print(d, "was deleted. No more Whois information available.")
        
