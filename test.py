import smtplib
import base64

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from_address = "martianchronicles1990@gmail.com"
to_address = "rahulrajesh2101@gmail.com"
password = "xmlnhzmyldtmoupw"

message = MIMEMultipart()
message["Subject"] = "Test Email with Image Attachment from Python"
message["From"] = from_address
message["To"] = to_address

text = MIMEText("This is a test email sent from Python with an image attachment.")
message.attach(text)

with open("photo1.jpg", "rb") as image:
    image_data = image.read()
    image_encoded = base64.b64encode(image_data)
    image = MIMEImage(image_data)
    message.attach(image)

server = smtplib.SMTP("smtp.gmail.com", 587) # replace "smtp.example.com" with the hostname of your SMTP server
server.ehlo()
server.starttls()
server.login(from_address, password)
server.sendmail(from_address, to_address, message.as_string())
server.quit()
