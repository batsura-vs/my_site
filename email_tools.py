import email.message as mail
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailTools:
    def __init__(self, email):
        self.email = email

    def check_username(self):
        email = self.email
        username = email.split('@')[0].lower()
        flag = True
        available = list('abcdefghijklmnopqrstuvwxyz0123456789.')
        if len(username) < 6 or len(username) > 30 or '..' in username:
            flag = False
        else:
            if list(username)[0] == available[-1] or list(username)[-1] == available[-1]:
                flag = False
        for i in username:
            if i not in available:
                flag = False
        return flag

    def check_domain(self, criteria):
        email = self.email
        domain = email.split('@')[1]
        flag = False
        if domain in criteria:
            flag = True
        return flag

    def is_valid(self, domains):
        email = self.email
        li = email.split('@')
        if len(li) == 2 and self.check_username() and self.check_domain(domains):
            return True
        return False

    def send_email(self, subject, from_, html, gmail, password):
        to = self.email
        msg = MIMEMultipart()  # Создаем сообщение
        msg['From'] = from_  # Адресат
        msg['To'] = to  # Получатель
        msg['Subject'] = subject  # Тема сообщения
        msg.attach(MIMEText(html, 'html', 'utf-8'))

        s = smtplib.SMTP('smtp.gmail.com')
        s.starttls()
        s.login(gmail, password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
