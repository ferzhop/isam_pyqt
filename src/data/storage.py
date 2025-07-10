import json
import os

class SimpleStorage:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f)
    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    def save(self, data):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
