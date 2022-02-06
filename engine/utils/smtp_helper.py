import smtplib
from email.mime.text import MIMEText
from email.header import Header

class Smtp(object):
    def __init__(self, mail_host, mail_user, mail_pass, is_ssl=True, port=587):
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.port = port
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

def notify_approvers(input_form_id, approvers):

    mail_host = "smtp.torro.ai"  # 设置服务器
    mail_user = "torroAdmin@torro.ai"  # 用户名
    mail_pass = "xxxxxxxxxx"  # 口令
    sender = 'torroAdmin@torro.ai'
    smtp = Smtp(mail_host, mail_user, mail_pass)
    subject = 'Torro - You have an approval ticket.'
    text = 'the waiting for approval form id is: %s' % input_form_id
    smtp.send_email(subject, text, receivers=approvers)
    data = {}
    return data