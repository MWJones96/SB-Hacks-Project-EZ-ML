import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from constants import FROMADDR, FROMPASS


fromaddr = FROMADDR
frompass = FROMPASS

def sendMessage( toaddr ,subject="",body="",attachment_url=""):
    msg = MIMEMultipart()
    
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    
    
    msg.attach(MIMEText(body, 'plain'))
    
    filename = ""
    attachment = open("/Users/Darren/Downloads/1.jpg", "rb")
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "PASSWORD")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
