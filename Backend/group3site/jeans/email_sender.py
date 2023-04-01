import smtplib
from django.template import loader


def send_promo_email(id, email_list):
    gmail_user = 'jeansyfajaspromos@gmail.com'
    gmail_password = 'hnhzjfajwiorxuju'

    sent_from = gmail_user
    to = [email_list]
    subject = 'Test for Promotional Emails'
    body = 'This is a test'

    template = loader.get_template('jeans/promo.html')
    email_text = "Testing 123"
    context = {}
    template.render(context)
    print(template)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)


def send_promo_email_test(id):
    send_promo_email(id, ["brettmeirhofer@gmail.com", ])

def main():
    send_promo_email(None, ["brettmeirhofer@gmail.com", ])


if __name__ == "__main__":
    main()
