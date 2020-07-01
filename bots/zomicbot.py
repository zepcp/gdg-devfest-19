import time
import peewee

from models import zomic as db
from settings import OFFSET, SLEEP, SMTP, DATE, ZOMIC_URL
from parsers.types import is_id
from utils.telegram import Bot
from utils.types import datetime_to_string

ZOMIC = Bot(ZOMIC_URL)

START = """
Hey! I'm ZomicBot and I'm here to help you engage with your community
I can help you out with one of the below options:
/my_chat_ID
/my_communities
/my_proposals
/get_proposal_ID
/get_help
"""

NO_COMMUNITIES = "No communities found, have you enrolled in any community?"
NO_PROPOSALS = "No proposals found, have you enrolled in any community?"
UNKNOWN_ID = "Don't know that ID, are you sure it is the right one?"
UNKNOWN = "I don't understand your request, try /start or /get_help"
HELP = "If you need further assistance send it to {}".format(SMTP["user"])


def last_msg():
    return ZOMIC.get()[-1]['update_id'] if ZOMIC.get() else OFFSET


def subscribed(chat_id):
    query = db.NewsletterTelegram.select().distinct(
        db.NewsletterTelegram.community_id).where(
        db.NewsletterTelegram.chat_id == chat_id).execute()

    response = []
    for sub in query:
        response.append(sub.community_id)
    return response


def my_print(my_table, community_id, my_communities):
    query = my_table.select().where(
        community_id in my_communities).execute()

    response = ""
    for my_id in query:
        response += "/get_" + str(my_id.id) + "\n"
    return response


def get_proposal(value):
    text = "Community: " + str(value.community_id)
    text += "\nTitle: " + str(value.title)
    text += "\nStatus: " + str(value.status)
    if value.status != "Open":
        text += "\nIn Favor: " + str(value.in_favor)
        text += "\nAgainst: " + str(value.against)
    text += "\nApproval Rate: " + str(value.approval_rate)
    text += "\nDeadline: " + datetime_to_string(value.deadline, DATE)
    text += "\nType: " + str(value.type)
    text += "\nDescription: " + str(value.description)
    return text


def get_community(value):
    text = "Name: " + str(value.name)
    text += "\nInfo: " + str(value.required_info)
    text += "\nFounder: " + str(value.founder)
    text += "\nPermissions: " + str(value.permissions)
    return text


def parse_message(user, text, communities):
    if text == "/start":
        ZOMIC.send(user, text=START)

    elif text == "/my_chat_ID":
        ZOMIC.send(user, text=user)

    elif text == "/my_communities":
        answer = my_print(db.Community,
                          db.Community.id, communities)
        ZOMIC.send(user, text=answer if answer else NO_COMMUNITIES)

    elif text == "/my_proposals":
        answer = my_print(db.Proposal,
                          db.Proposal.community_id, communities)
        ZOMIC.send(user, text=answer if answer else NO_PROPOSALS)

    elif text[0:5] == "/get_" and is_id(text[5:]):
        try:
            answer = db.Proposal.get(
                db.Proposal.id == text[5:],
                db.Proposal.community_id in communities)
            ZOMIC.send(user, text=get_proposal(answer))
        except peewee.DoesNotExist:
            try:
                answer = db.Community.get(
                    db.Community.id == text[5:])
                ZOMIC.send(user, text=get_community(answer))
            except peewee.DoesNotExist:
                ZOMIC.send(user, text=UNKNOWN_ID)

    elif text == "/get_help":
        ZOMIC.send(user, text=HELP)

    else:
        ZOMIC.send(user, text=UNKNOWN)


if __name__ == "__main__":
    last_msg = last_msg()
    last_time = time.time()
    while True:
        for msg in ZOMIC.get(last_msg):
            if msg["update_id"] <= last_msg:
                continue

            try:
                message = msg["message"]
            except KeyError:
                message = msg["edited_message"]

            try:
                parse_message(message["from"]["id"], message["text"],
                              subscribed(message["from"]["id"]))
                last_time = time.time()
            except KeyError:
                continue
            last_msg = msg["update_id"]

        time.sleep(max(SLEEP["min"], min((time.time()-last_time)/SLEEP["step"], SLEEP["max"])))
