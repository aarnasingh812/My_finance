import configparser
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


config = configparser.ConfigParser()
config.read("config.ini")

def sendMailusingSendgrid(API, from_email, to_email, subject, html_content, attachment_path=None):
    if API!=None and from_email!=None and len(to_email)>0:
        message = Mail(from_email, to_email, subject, html_content)
        try:
            sg = SendGridAPIClient(API)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print("error occured")
            print(e.message)


    
try:
    settings = config["SETTINGS"]
except:
    settings = {}

API = settings.get("APIKEY",None)
from_email = settings.get("FROM",None)
#to_email = settings.get("TO","")

subject = "New account created"
html_content = "Welcome on board. I hope you like our platform"

def recipent(receiver):
    to_email=receiver
    sendMailusingSendgrid(API,from_email,to_email,subject,html_content)
