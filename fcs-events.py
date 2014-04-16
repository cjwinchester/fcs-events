from mechanize import Browser
from bs4 import *
import re
import datetime
import smtplib

# configure mechanize
mech = Browser()
mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
mech.set_handle_robots(False)

# munge today's url
base = "http://www.nrc.gov/reading-rm/doc-collections/event-status/event/"
today = datetime.date.today()
year = str(today.year)

if len(str(today.month)) == 1:
    month = '0' + str(today.month)
else:
    month = str(today.month)

if len(str(today.day)) == 1:
    day = '0' + str(today.day)
else:
    day = str(today.day)

url = base + year + "/" + year + month + day + "en.html"

# soup the page
page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

# does "Fort Calhoun" appear?
fcs = soup.find(text=re.compile("fort calhoun", re.IGNORECASE))

# if so, send me an email, please
if fcs:
    table = fcs.parent.parent.parent.parent.findAll('table')[2]
    iso = str(table).split("<br>")[0].strip().replace('<table border="1" cellpadding="3" cellspacing="0" width="98%">\n<tr>\n','').replace('<td align="left" scope="row">','')
    find_date = re.search(r'Notification Date: \d\d/\d\d/\d\d\d\d', str(fcs.parent.parent))
    this_date = find_date.group().replace('Notification Date: ','')
    text = 'Dear Future Cody:\n\nOn ' + this_date + ', OPPD reported an event at Fort Calhoun: ' + iso + '.\n\n' + url + "\n\nSincerely,\nPast Cody"
    fromaddr = 'cjwinchester@gmail.com'
    toaddrs = 'cjwinchester@gmail.com'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('cjwinchester@gmail.com', 'xxxxxxxxxxxxxxxxxx')
    msg = ("From: cjwinchester@gmail.com\r\nTo: cjwinchester@gmail.com\r\nSubject: Something happened at the Fort Calhoun Nuclear Station\r\n\r\n")
    msg = msg + text
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
else:
    pass
