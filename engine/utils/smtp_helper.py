import smtplib
from email.mime.text import MIMEText
from email.header import Header
from db.org.db_org_mgr import org_mgr
from utils.status_code import response_code
from common.common_crypto import prpcrypt
import os
from config import config
import traceback
import logging

logger = logging.getLogger("main." + __name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]

class Smtp(object):
    def __init__(self, ):
        mail_host, mail_user, mail_pass, mail_port, is_tls = org_mgr.get_smtp()
        self.mail_host = mail_host
        self.mail_user = mail_user
        try:
            self.mail_pass = prpcrypt.decrypt(mail_pass)
        except:
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
            logger.debug("FN:Smtp_send_email sender:{} receivers:{} message:{}".format(sender, receivers, message.as_string()))
            smtpObj.sendmail(sender, receivers, message.as_string())
            return True
        except smtplib.SMTPException:
            logger.error("FN:Smtp_send_email error:{}".format(traceback.format_exc()))
            return False

    @staticmethod
    def check_email_pwd(mail_host, mail_user, mail_pass, mail_port, mail_tls):
        try:
            logger.debug("FN:Smtp_check_email_pwd mail_host:{} mail_user:{} mail_port:{} mail_tls:{}".format(mail_host, mail_user, mail_port, mail_tls))
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, mail_port)
            smtpObj.ehlo()
            if mail_tls == 1:
                smtpObj.starttls()
            try:
                mail_pass = prpcrypt.decrypt(mail_pass)
            except:
                mail_pass = mail_pass

            smtpObj.login(mail_user, mail_pass)
            # smtpObj.sendmail(sender, receivers, message.as_string())
            logger.debug("FN:Smtp_check_email_pwd check_success:True")

            return True
        except smtplib.SMTPException:
            logger.error("FN:Smtp_check_email_pwd error:{}".format(traceback.format_exc()))
            return False
        
def notify_approvers(input_form_id, approvers, text=None):
    approvers = list(set(approvers))
    logger.info("FN:Smtp_notify_approvers input_form_id:{} approvers:{}".format(input_form_id, approvers))
    smtp = Smtp()
    logger.debug("FN:Smtp_notify_approvers mail_host:{} mail_user:{} mail_tls:{}".format(smtp.mail_host,smtp.mail_user,smtp.is_tls))
    # return response_code.SUCCESS
    
    # Change the subject line for your company specific line
    subject = 'Torro - You have an new ticket message await your action'
    if not text:
        text = 'The waiting for approval form id is: %s' % input_form_id
        text += '\n URL: '+Config.FRONTEND_URL+'/app/approvalFlow?id=%s' % input_form_id

    logger.debug("FN:Smtp_notify_approvers subject:{} body:{} receivers:".format(subject, text, approvers))
    smtp.send_email(subject, text, receivers=approvers)
    data = response_code.SUCCESS
    logger.debug("FN:Smtp_notify_approvers email_sent:True")
    
    return data
