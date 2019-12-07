import models

from safe import SMTP_HOST, SMTP_USER, SMTP_PASS
from utils.telegram import Bot
from utils.mail import Mail


def send_by_mail(subject, message, to_address):
    return Mail(SMTP_HOST, SMTP_USER, SMTP_PASS).send_mail(subject, message, to_address)


def send_by_telegram(subject, message, telegram_id):
    Bot().send(telegram_id, subject)
    return Bot().send(telegram_id, message)


def send_proposal(proposta_id):
    subject = "Nova Proposta - " + str(proposta_id)
    message = "Details"

    mail_list = models.NewsletterEmail.select().where().execute()
    telegram_list = models.NewsletterTelegram.select().where().execute()

    for to_address in mail_list:
        send_by_mail(subject, message, to_address)

    for telegram_id in telegram_list:
        send_by_telegram(subject, message, telegram_id)
    return


def send_result(proposta_id, result, in_favor, against, txid):
    subject = "Proposta - " + str(proposta_id) + ": " + result
    message = "Votos a Favor: {}\nVotos Contra: {}\nTxID: {}".format(str(in_favor),
                                                                     str(against),
                                                                     txid)

    mail_list = models.NewsletterEmail.select().execute()
    telegram_list = models.NewsletterTelegram.select().execute()

    for mail in mail_list:
        send_by_mail(subject, message, mail.email)

    for telegram in telegram_list:
        send_by_telegram(subject, message, telegram.id)
    return
