from bs4 import BeautifulSoup # used to scrape html part of email
import email.parser # used to parse headers, body from email
import sys # used to get argument (email file)
import re # used to catch IP address
#
# To ensure all necessary modules are installed: pip install -r requirements.txt
#
# manage argument passed in command line: python parsEmail.py emailFileToBeProcessed.eml
file = sys.argv[1]
#path_file = os.path.split(file)[0]
#
receivedFrom = {} # dictionary for received header split contents
tmpIp = ''
#
def extReceived(received): # used to split "received" header contents
    receive = {}
    receive = received.split()
    return receive 

with open(file, 'r') as myMail:
    msg = email.parser.Parser().parse(myMail, True) # parse email file (myMail)  to retrieve only headers: True

taille_msg = len(msg)

for k,v in msg.items():
    try:
        tmpIp = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', v).group()
    except:
        tmpIp = ''
    if k == 'Received':
        temp = extReceived(v)
        idx_by = temp.index('by')
        receivedFrom["Received"] = temp[1]
        receivedFrom["IP"] = tmpIp
        receivedFrom["Date"] = v.split(';')[1]
        receivedFrom["By"] = temp[idx_by + 1]
#
# Display Report
#
print("===") 
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
#
print("Message Body analysis")
print("=====================")
msg_html = open(file, "r")
soup = BeautifulSoup(msg_html, 'lxml')
for link in soup.findAll('a'):
    if link.string != None:
        print("<",link.string,">")
        print("Initial Link:", link.get('href'))




