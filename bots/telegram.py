"""Telegram utils"""
import os
import requests
from settings import BOT_URL


class Bot:
    """Telegram bot class, get and send info"""
    def __init__(self):
        self.base_url = BOT_URL

    def get_url(self, params=None):
        """Get Telegram URL"""
        if not params:
            return os.path.join(self.base_url, "getUpdates")
        query = "sendSticker" if "sticker" in params else \
                "sendPhoto" if "photo" in params else "sendMessage"
        return os.path.join(self.base_url, query)

    @staticmethod
    def get_params(chat, text=None, sticker=None, photo=None):
        """Parse sent info as params"""
        params = {"chat_id": chat}
        if sticker:
            params["sticker"] = sticker
        elif photo:
            params["photo"] = photo
            params["caption"] = text
        elif text:
            params["text"] = text
        return params

    def send(self, chat, text=None, sticker=None, photo=None):
        """Send info to telegram chat"""
        params = self.get_params(chat, text, sticker, photo)
        res = requests.get(self.get_url(params), params=params)
        # Cant send sticker and text simultaneously
        if sticker and text:
            params = self.get_params(chat, text)
            res = requests.get(self.get_url(params), params=params)
        return res.json()["ok"] if res.status_code == 200 else False

    def get(self, offset=0):
        """Receive info sent to telegram bot"""
        res = requests.get(self.get_url(), params={"offset": offset})
        return res.json()["result"] if res.status_code == 200 else False
