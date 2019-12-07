import time

from utils.telegram import Bot
from settings import OFFSET, TELEGRAM_SLEEP

ZOMIC = Bot()


def last_msg():
    return ZOMIC.get()[-1]['update_id'] if ZOMIC.get() else OFFSET


def mirror_content(_message):
    try:
        ZOMIC.send(user, text=_message["text"])
    except KeyError:
        pass

    try:
        ZOMIC.send(user, sticker=_message["sticker"]["file_id"])
    except KeyError:
        pass

    try:
        ZOMIC.send(user, sticker=_message["animation"]["file_id"])
    except KeyError:
        pass

    try:
        try:
            caption = _message["caption"]
        except KeyError:
            caption = None
        ZOMIC.send(user, text=caption, photo=_message["photo"][0]["file_id"])
    except KeyError:
        pass


if __name__ == "__main__":
    last_msg = last_msg()
    update_id = 0
    while True:
        for msg in ZOMIC.get(update_id):
            # Msg Already Processed
            if msg["update_id"] <= last_msg:
                continue

            try:
                message = msg["message"]
            except KeyError:
                message = msg["edited_message"]

            user = message["from"]["id"]
            username = message["from"]["username"]
            first_name = message["from"]["first_name"]
            last_name = message["from"]["last_name"]

            print(user, username, first_name, last_name)
            print(message)
            mirror_content(message)

            last_msg = msg["update_id"]
        time.sleep(TELEGRAM_SLEEP)
