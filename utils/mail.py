"""Email Interface"""
import smtplib

from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class Mail:
    """Email Interface"""
    def __init__(self, host, email, pwd, port=587):
        self.SMTP_HOST = host
        self.SMTP_USER = email
        self.SMTP_PASS = pwd
        self.SMTP_PORT = port

    def send_mail(self, subject, message, to_address, from_address=None,
                  attachments=None, html=False):
        """MIMEMultipart creates a text/plain message"""
        msg = MIMEMultipart("mixed")

        msg["Subject"] = subject
        msg["To"] = ",".join(to_address)
        from_addr = self.SMTP_USER if not from_address else from_address
        msg.attach(MIMEText(message, "html" if html else "plain"))

        if attachments:
            for file in attachments:
                with open(file, "rb") as fil:
                    msg.attach(MIMEApplication(
                        fil.read(),
                        Content_Disposition='attachment; filename="%s"' % file,
                        Name=basename(file)))

        server = smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.SMTP_USER, self.SMTP_PASS)
        server.sendmail(from_addr, to_address, msg.as_string())
        server.quit()
