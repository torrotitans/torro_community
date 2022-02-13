import smtplib
from email.mime.text import MIMEText
from email.header import Header
from db.org.db_org_mgr import org_mgr
from utils.status_code import response_code
from common.common_crypto import prpcrypt
class Smtp(object):
    def __init__(self, ):
        mail_host, mail_user, mail_pass, is_ssl, port = org_mgr.get_smtp()
        self.mail_host = mail_host
        self.mail_user = mail_user
        try:
            self.mail_pass = prpcrypt.encrypt(mail_pass)
        except:
            print('encrypt: ', mail_pass)
            self.mail_pass = ''
        self.port = port
        if int(is_ssl) == 1:
            is_ssl = True
        else:
            is_ssl = False
        self.is_ssl = is_ssl

    def send_email(self, subject, text, receivers, sender=None, sender_name=None):

        if sender is None:
            sender = self.mail_user
        if sender_name is None:
            sender_name = 'TorroAdmin'
        message = MIMEText(text, 'plain', 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        if sender_name:
            message['From'] = Header(sender_name, 'utf-8')
        else:
            message['From'] = Header(sender, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, self.port)
            smtpObj.ehlo()
            if self.is_ssl:
                smtpObj.starttls()
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            return True
        except smtplib.SMTPException:
            import traceback
            # print(traceback.format_exc())
            return False

def notify_approvers(input_form_id, approvers, text=None):
    print('Email info:', input_form_id, approvers, text)
    return response_code.SUCCESS
    smtp = Smtp()
    subject = 'Torro - You have an new ticket message.'
    if not text:
        text = 'The waiting for approval form id is: %s' % input_form_id
    smtp.send_email(subject, text, receivers=approvers)
    data = response_code.SUCCESS
    return data