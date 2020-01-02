from models import zomic as db

from settings import SMTP, ZOMIC_URL
from utils.telegram import Bot
from utils.mail import Mail


def send_by_mail(subject, message, to_address):
    return Mail(SMTP).send_mail(subject, message, to_address)


def send_by_telegram(subject, message, telegram_id):
    Bot(ZOMIC_URL).send(telegram_id, subject)
    return Bot(ZOMIC_URL).send(telegram_id, message)


def send_proposal(proposta_id):
    subject = "New Proposal - " + str(proposta_id)
    message = "Details"

    mail_list = db.NewsletterEmail.select().where().execute()
    telegram_list = db.NewsletterTelegram.select().where().execute()

    for to_address in mail_list:
        send_by_mail(subject, message, to_address)

    for telegram_id in telegram_list:
        send_by_telegram(subject, message, telegram_id)
    return


def send_result(proposta_id, result, in_favor, against, txid):
    subject = "Proposal - " + str(proposta_id) + ": " + result
    message = "Votes in Favor: {}\nVotes Against: {}\nTxID: {}".format(str(in_favor),
                                                                       str(against),
                                                                       txid)

    mail_list = db.NewsletterEmail.select().execute()
    telegram_list = db.NewsletterTelegram.select().execute()

    for mail in mail_list:
        send_by_mail(subject, message, mail.email)

    for telegram in telegram_list:
        send_by_telegram(subject, message, telegram.id)
    return
