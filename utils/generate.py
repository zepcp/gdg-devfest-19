import random
import string

from settings import LENGTHS


def random_id(length=LENGTHS["id"]):
    return ''.join(random.choices(string.ascii_letters + string.digits,
                                  k=length))
