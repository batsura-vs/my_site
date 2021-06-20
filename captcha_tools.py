import requests


class HCaptcha:
    def __init__(self, token, secret_key):
        self.token = token
        self.secret_key = secret_key

    def verify(self):
        resp = requests.post('https://hcaptcha.com/siteverify',
                             data={"response": self.token, "secret": self.secret_key}).json()
        return resp['success']
