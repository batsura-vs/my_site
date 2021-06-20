import json
import secrets


class SetSettings:
    def __init__(self, file_path, app):
        with open(file_path, 'r') as f:
            self.settings = json.loads(f.read())
        self.app = app

    def use(self):
        self.app.config["SECRET_KEY"] = secrets.token_urlsafe(30)
        for i in self.settings.keys():
            self.app.config[i] = self.settings[i]
