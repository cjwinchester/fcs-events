import requests
from bs4 import *
import re
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

d = datetime.datetime.now()
year = d.strftime("%Y") 
patt = d.strftime('%Y%m%den')
url = "http://www.nrc.gov/reading-rm/doc-collections/event-status/event/" + year +"/" + patt + ".html"
r = requests.get(url)
soup = BeautifulSoup(r.text)
fcs = soup.find(text=re.compile("fort calhoun", re.IGNORECASE))

def sendMeAnEmail():
    me = 'worldheraldbot@gmail.com'
    you = ['cody.winchester@owh.com']
    pw = #pw here
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Fort Calhoun Event'
    msg['From'] = "Fort Calhoun Events Bot"
    html = "<html><head><style>* { font-family:Verdana,sans-serif }</style></head><body>" + "Something happened at FCS you might want to check out, yo: " + url + "</body></html>"
    wut = MIMEText(html, 'html')
    msg.attach(wut)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(me, pw)
    server.sendmail(me, you, msg.as_string())
    server.quit()
    
if fcs:
    sendMeAnEmail()