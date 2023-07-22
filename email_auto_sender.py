import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import csv

smtp_port = 587
smtp_server = 'smtp.gmail.com'


def send_emails(email_list, email_body_plain, email_body_html):
    print("Connecting to server...")

    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from, email_password)
    print("Succesfully connected to server")
    print()
    for email_to in email_list:

        msg = MIMEMultipart('alternative')
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = email_subject

        msg.attach(MIMEText(email_body_plain, 'plain'))
        msg.attach(MIMEText(email_body_html, 'html'))

        filename = "attachment.jpg"
        attachment = open(filename, "rb")

        attachment_package = MIMEBase('application', 'octet-system')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header(
            'Content-Disposition', 'attachment; filename= ' + filename)
        msg.attach(attachment_package)

        text = msg.as_string()

        print(f'Sending email to: {email_to}...')
        TIE_server.sendmail(email_from, email_to, text)
        print(f"Email sent to: {email_to}")
        print()

    TIE_server.quit()


email_list = []
# Email extractor
with open('emails.csv') as f:
    reader = csv.reader(f)
    data = list(reader)
    for email in data:
        email_list.append(email[0])

email_list = list(dict.fromkeys(email_list))  # Remove duplicates
print(f'Size: {len(email_list)} emails')

email_from = ''  # Your email
email_password = ''  # Your password from https://myaccount.google.com/apppasswords


email_subject = 'subject'
email_body_plain = """
text
"""
email_body_html = """
<html>
  <head></head>
  <body>
    <p>text</p>
  </body>
</html>
"""


send_emails(email_list, email_body_plain, email_body_html)
