import re
import logging
from collections import OrderedDict

import redis

from django.conf import settings
from rest_framework.utils.serializer_helpers import ReturnList

from musikhar.abstractions.messages import ErrorMessaging

MOBILE_RE = re.compile(r"^[0-9]{11}$")
EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
Errors = ErrorMessaging()

CONTENT_TYPE_IMAGE = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif'
}
CONTENT_TYPE_AUDIO = 'audio/mpeg'

app_logger = logging.getLogger('application')
err_logger = logging.getLogger('error')


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


def conn():
    return redis.Redis(host='localhost', port=settings.REDIS_PORT, db=1)


def convert_to_dict(ordered_dict):
    # print('processing \n {}'.format(ordered_dict))
    err_logger.info('[CACHE] processing \n {}'.format(str(ordered_dict).encode('utf8')))
    if isinstance(ordered_dict, OrderedDict):
        res = dict(ordered_dict)
    else:
        res = ordered_dict

    for key in res:
        # print('type of key: {} is {}'.format(key, type(res[key])))
        err_logger.info('[CACHE] type of key: {} is {}'.format(key, type(res[key])))
        if isinstance(res[key], OrderedDict) or isinstance(res[key], dict):
            res[key] = convert_to_dict(res[key])
        elif isinstance(res[key], list) or isinstance(res[key], ReturnList):
            origin_list = res[key]
            res[key] = []
            for node in origin_list:
                res[key].append(convert_to_dict(node))
    # print('result of this: \n {} is this: \n {}'.format(ordered_dict, res))
    err_logger.info('[CACHE] result of this: \n {} is this: \n {}'.format(str(ordered_dict).encode('utf8'), res))
    err_logger.info('[CACHE] result is: {}'.format(res))
    return res

