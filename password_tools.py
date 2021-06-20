import hashlib


class PasswordTools:
    def __init__(self, password):
        self.password = password

    def check_password(self, min_length, max_length):
        password = self.password
        flag = True
        if min_length > len(password) or len(password) > max_length:
            flag = False
        return flag

    def hash(self):
        return int(hashlib.md5(self.password.encode('utf-8')).hexdigest(), 16)
