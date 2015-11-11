# -*- coding: utf-8 -*-

__author__ = 'yw'

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email import encoders
from email.utils import parseaddr, formataddr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))


class SendMail(object):
    def __init__(self, config):
        super(SendMail, self).__init__()
        server_config = config['server']
        mail_config = config['mail']
        self._user = server_config['user']
        self._pwd = server_config['password']
        self._subject = mail_config['subject']
        self._from = mail_config['from']
        self._to = mail_config['to']
        self._port = server_config['port']
        self._smtp_server = server_config['smtp']
        self._is_ssl = server_config['isSSL']

    @property
    def server(self):
        if not hasattr(self, '_server'):
            self._server = smtplib.SMTP_SSL(self._smtp_server, port=self._port) if self._is_ssl else smtplib.SMTP(
                self._smtp_server, port=self._port)
            self._server.login(self._user, self._pwd)
        return self._server

    def gen_msg(self, content):
        msg = MIMEText('<html><body>{}</body></html>'.format(content), 'html', 'utf-8')
        msg['Subject'] = Header(self._subject, 'utf-8').encode()
        msg['From'] = _format_addr(u'下载机器人 <%s>' % self._from)
        msg['To'] = _format_addr(u'管理员 <%s>' % self._to)
        return msg

    def send_mail(self, content):
        self.server.sendmail(self._from, self._to, self.gen_msg(content).as_string())

    def __del__(self):
        self.server.quit()
