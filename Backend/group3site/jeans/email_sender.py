import smtplib
from email.message import EmailMessage


smtp_server = "smtp.gmail.com" #server address
smtp_port = 465 #port number
Email = "idahbest@gmail.com" #sender email
Pass = "aB@Y6GCYX" #sender password


Contacts = ["seth.i.esparza@gmail.com"]


message = EmailMessage()
message["Subject"] = "Test Message"
message["From"] = Email #Sender email
message["To"] = Contacts #Receiver email
message.set_content("This is just a Test Message")
    
message.add_alternative("""\
    
    
    
""", subtype="html")


with smtplib.STMP_SSL(smtp_server, smtp_port) as smtp:
    smtp.login(Email, Pass)
    smtp.send_message(message) 