import smtplib
from email.mime.text import MIMEText
from email.header import Header
from db.org.db_org_mgr import org_mgr
from utils.status_code import response_code
from common.common_crypto import prpcrypt
class Smtp(object):
    def __init__(self, ):
        mail_host, mail_user, mail_pass, mail_port, is_tls = org_mgr.get_smtp()
        self.mail_host = mail_host
        self.mail_user = mail_user
        try:
            self.mail_pass = prpcrypt.decrypt(mail_pass)
        except:
            print('Email encrypt: ', mail_pass)
            self.mail_pass = mail_pass
        # self.port = port
        if int(is_tls) == 1:
            is_tls = True
        else:
            is_tls = False
        self.is_tls = is_tls
        self.port = mail_port
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
            if self.is_tls is True or self.is_tls == 1:
                smtpObj.starttls()
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            return True
        except smtplib.SMTPException:
            import traceback
            # print(traceback.format_exc())
            return False

    @staticmethod
    def check_email_pwd(mail_host, mail_user, mail_pass, mail_port, mail_tls):
        try:
            print('smtp info:', mail_host, mail_user, mail_pass, mail_port, mail_tls)
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, mail_port)  # 25 为 SMTP 端口号
            smtpObj.ehlo()
            if mail_tls == 1:
                smtpObj.starttls()

            try:
                mail_pass = prpcrypt.decrypt(mail_pass)
            except:
                print('Email encrypt: ', mail_pass)
                mail_pass = mail_pass

            smtpObj.login(mail_user, mail_pass)
            # smtpObj.sendmail(sender, receivers, message.as_string())
            # print("邮件发送成功")
            return True
        except smtplib.SMTPException:
            import traceback
            print(traceback.format_exc())
            return False
def notify_approvers(input_form_id, approvers, text=None):
    approvers = list(set(approvers))
    print('Email info:', input_form_id, approvers, text)
    smtp = Smtp()
    print('Email client:', smtp.mail_host,smtp.mail_user, smtp.mail_pass, smtp.is_tls)
    # return response_code.SUCCESS

    subject = 'Torro - You have an new ticket message.'
    if not text:
        text = 'The waiting for approval form id is: %s' % input_form_id
    smtp.send_email(subject, text, receivers=approvers)
    data = response_code.SUCCESS
    return data