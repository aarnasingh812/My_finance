import base64
import mimetypes
import configparser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

# Load config
config = configparser.ConfigParser()
config.read("config.ini")

try:
    settings = config["SETTINGS"]
except KeyError:
    settings = {}

API = settings.get("APIKEY", None)
from_email = settings.get("FROM", None)
to_email = "tina.aar2002@gmail.com"

subject = "Hello with NEW Attachment"
html_content = "<strong>Here's your attachment</strong>"

def sendMailusingSendgrid(API, from_email, to_email, subject, html_content, attachment_path=None):
    if API and from_email and to_email:
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )

        # Add attachment using mimetypes
        if attachment_path:
            try:
                with open(attachment_path, 'rb') as f:
                    data = f.read()
                    encoded_file = base64.b64encode(data).decode()

                # Use mimetypes to guess file type
                mime_type, _ = mimetypes.guess_type(attachment_path)
                mime_type = mime_type or "application/octet-stream"

                attachment = Attachment(
                    FileContent(encoded_file),
                    FileName(attachment_path.split("/")[-1]),
                    FileType(mime_type),
                    Disposition("attachment")
                )
                message.attachment = attachment
            except Exception as file_error:
                print(f"⚠️ Could not attach file: {file_error}")
                return

        try:
            sg = SendGridAPIClient(API)
            response = sg.send(message)
            if response.status_code == 202:
                print("✅ Email with attachment sent successfully!")
            else:
                print(f"❌ Failed with status code: {response.status_code}")
        except Exception as e:
            print("Error occurred:")
            print(str(e))

# Example usage
attachment_path = "my_file.pdf"  # Replace with your file
sendMailusingSendgrid(API, from_email, to_email, subject, html_content, attachment_path)
