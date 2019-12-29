import time
import models
import peewee

from settings import OFFSET, TELEGRAM_SLEEP, SMTP_USER, DATE
from parsers.types import is_id
from utils.telegram import Bot
from utils.types import datetime_to_string

ZOMIC = Bot()

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
HELP = "If you need further assistance send it to {}".format(SMTP_USER)


def last_msg():
    return ZOMIC.get()[-1]['update_id'] if ZOMIC.get() else OFFSET


def subscribed(chat_id):
    query = models.NewsletterTelegram.select().distinct(
        models.NewsletterTelegram.community_id).where(
        models.NewsletterTelegram.chat_id == chat_id).execute()

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
    text += "\nLevels: " + str(value.levels)
    text += "\nPermissions: " + str(value.permissions)
    return text


def parse_message(user, text, communities):
    if text == "/start":
        ZOMIC.send(user, text=START)

    elif text == "/my_chat_ID":
        ZOMIC.send(user, text=user)

    elif text == "/my_communities":
        answer = my_print(models.Community,
                          models.Community.id, communities)
        ZOMIC.send(user, text=answer if answer else NO_COMMUNITIES)

    elif text == "/my_proposals":
        answer = my_print(models.Proposal,
                          models.Proposal.community_id, communities)
        ZOMIC.send(user, text=answer if answer else NO_PROPOSALS)

    elif text[0:5] == "/get_" and is_id(text[5:]):
        try:
            answer = models.Proposal.get(
                models.Proposal.id == text[5:],
                models.Proposal.community_id in communities)
            ZOMIC.send(user, text=get_proposal(answer))
        except peewee.DoesNotExist:
            try:
                answer = models.Community.get(
                    models.Community.id == text[5:])
                ZOMIC.send(user, text=get_community(answer))
            except peewee.DoesNotExist:
                ZOMIC.send(user, text=UNKNOWN_ID)

    elif text == "/get_help":
        ZOMIC.send(user, text=HELP)

    else:
        ZOMIC.send(user, text=UNKNOWN)


if __name__ == "__main__":
    last_msg = last_msg()
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
            except KeyError:
                continue
            last_msg = msg["update_id"]

        time.sleep(TELEGRAM_SLEEP)
