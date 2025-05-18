import yaml
from logger import logger

class TextResources:
    def __init__(self, path="text-resources.yml"):
        with open(path, "r", encoding="utf-8") as f:
            self.texts = yaml.safe_load(f)

    def get(self, *keys):
        current = self.texts
        for key in keys:
            if key in current:
                current = current[key]
            else:
                logger.info(f"Key(s) '{'.'.join(keys)}' not found in text resources.")
                return ""
        return current