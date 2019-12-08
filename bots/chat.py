import time

import models

from utils.telegram import Bot
from settings import OFFSET, TELEGRAM_SLEEP, SMTP_USER

ZOMIC = Bot()

START = """Olá! Sou o ZomicBot, estou aqui para te ajudar a participar na tua comunidade.
Consigo-te ajudar com estas opções:
/subscrever_newsletter
/cancelar_subscricao
/propostas
/info_proposta_ID
/ajuda"""
SUBSCRIBED = "Registado! Irás receber updates da comunidade"
UNSUBSCRIBED = "Registado! Vais deixar de receber updates da comunidade"
ALREADY_SUBSCRIBED = "Já estava registado! Estás a receber updates da comunidade"
ALREADY_UNSUBSCRIBED = "Já estava Registado! Não estás a receber updates da comunidade"
HELP = "Envia a tua questão para {}, tentarei responder assim que possível".format(SMTP_USER)
NO_PROPOSAL = "Não conheço o ID dessa proposta, tens a certeza que já foi submetida?"
UNKNOWN = "Olá, não reconheço esse comando, tenta /start ou /ajuda para mais informação"


def last_msg():
    return ZOMIC.get()[-1]['update_id'] if ZOMIC.get() else OFFSET


def parse_message(user, text):
    if text == "/start":
        ZOMIC.send(user, text=START)

    elif text == "/subscrever_newsletter":
        try:
            models.NewsletterTelegram.create(id=user)
            ZOMIC.send(user, text=SUBSCRIBED)
        except:
            models.db.close()
            ZOMIC.send(user, text=ALREADY_SUBSCRIBED)

    elif text == "/cancelar_subscricao":
        models.NewsletterTelegram.delete().where(models.NewsletterTelegram.id == user).execute()
        ZOMIC.send(user, text=UNSUBSCRIBED)

    elif text == "/propostas":
        proposals = models.Proposals.select().execute()
        response = ""
        for proposal in proposals:
            response += "/info_proposta_" + str(proposal.id) + "\n"
        ZOMIC.send(user, text=response)

    elif "/info_proposta_" in text:
        try:
            proposal_id = int(text.split("_")[2])
            proposal = models.Proposals.get(models.Proposals.id == proposal_id)

            ZOMIC.send(user, text="Titulo: "+str(proposal.title))
            ZOMIC.send(user, text="Tópico: "+str(proposal.topic))
            ZOMIC.send(user, text="Deadline: "+str(proposal.deadline)[:10])
            ZOMIC.send(user, text="Descrição: "+proposal.description)
        except (ValueError, IndexError):
            ZOMIC.send(user, text=NO_PROPOSAL)

    elif text == "/ajuda":
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
                parse_message(message["from"]["id"], message["text"])
            except KeyError:
                continue
            last_msg = msg["update_id"]

        time.sleep(TELEGRAM_SLEEP)
