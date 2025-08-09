import json

class SettingsReader:
    def __init__(self):
        self.load()

    def load(self):
        with open('settings.json', 'r') as file:
            self.data = json.load(file)
    
    def __getitem__(self, key):
        return self.data[key]
