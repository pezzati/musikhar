import re

from musikhar.abstractions.messages import ErrorMessaging

MOBILE_RE = re.compile(r"^[0-9]{11}$")
EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
Errors = ErrorMessaging()


def validate_cellphone(phone_no):
    if phone_no:
        if phone_no[0:3] == '+98':
            phone_no = phone_no[3:]

        if phone_no[0] != '0':
            phone_no = "0" + phone_no

        if phone_no[0:2] != '09':
            return False
        else:
            if MOBILE_RE.match(phone_no):
                return phone_no
            else:
                return False
    return False


def validate_email(mail):
    if EMAIL_RE.match(mail):
        return True
    return False


def get_not_none(dict, key, default=None):
    res = dict.get(key)
    if res is None:
        return default
    return res

