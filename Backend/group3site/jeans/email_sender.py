import smtplib

'''import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "dbms"
)

## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()

cursor.execute("SELECT email FROM customer WHERE status = 'ACTIVE'")''' 






gmail_user = 'jeansyfajaspromos@gmail.com'
gmail_password = 'hnhzjfajwiorxuju'

sent_from = gmail_user
to = ['seth.i.esparza@gmail.com']
subject = 'Test for Promotional Emails'
body = 'This is a test'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")
except Exception as ex:
    print ("Something went wrong….",ex)