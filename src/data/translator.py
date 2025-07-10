import json
import os

class Translator:
    def __init__(self, lang="es"):
        self.lang = lang
        self.translations = {}
        self.load_language(lang)

    def load_language(self, lang):
        path = os.path.join(os.path.dirname(__file__), "..", "resources", "lang", f"{lang}.json")
        with open(path, "r", encoding="utf-8") as f:
            self.translations = json.load(f)
        self.lang = lang

    def t(self, key):
        return self.translations.get(key, key)
