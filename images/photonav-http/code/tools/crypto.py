import time
import random
import string
import uuid
import hashlib


UID_RAND_INT_LENGTH = 30


def random_integer(length):
    return random.SystemRandom().randrange(10 ** length, 10 ** (length + 1))


def salt():

    salt = str(int(time.time()))
    salt += "-"
    salt += str(random_integer(8))
    salt += "-"
    salt += "".join(
        random.SystemRandom().choice(
            string.ascii_uppercase + string.digits
        )
        for _ in range(20))
    salt += "-"
    salt += str(uuid.uuid4())

    return salt


def user_id():
    return(
        str(int(time.time())) +
        "-" +
        str(uuid.uuid4()) +
        "-" +
        str(
            random.SystemRandom().randrange(
                10 ** UID_RAND_INT_LENGTH,
                10 ** (UID_RAND_INT_LENGTH + 1)
            )
        )
    )


def hash(password, user, salt):
    return hashlib.sha512(
        (password + user + salt).encode('utf-8')
    ).hexdigest()
