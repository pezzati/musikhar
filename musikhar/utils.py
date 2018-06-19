# -*- coding: utf-8 -*-

import re
import logging
from collections import OrderedDict
from kavenegar import *
import redis
import datetime
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

SMS_TEMPLATES = {
     'verify_number': 'VerifyNumber',
}

app_logger = logging.getLogger('application')
err_logger = logging.getLogger('error')
celery_logger = logging.getLogger('celery')


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
    # err_logger.info('[CACHE] processing \n {}'.format(str(ordered_dict).encode('utf8')))
    if isinstance(ordered_dict, OrderedDict):
        res = dict(ordered_dict)
    else:
        res = ordered_dict

    for key in res:
        # print('type of key: {} is {}'.format(key, type(res[key])))
        # err_logger.info('[CACHE] type of key: {} is {}'.format(key, type(res[key])))
        if isinstance(res[key], OrderedDict) or isinstance(res[key], dict):
            res[key] = convert_to_dict(res[key])
        elif isinstance(res[key], list) or isinstance(res[key], ReturnList):
            origin_list = res[key]
            res[key] = []
            for node in origin_list:
                res[key].append(convert_to_dict(node))
    # print('result of this: \n {} is this: \n {}'.format(ordered_dict, res))
    # err_logger.info('[CACHE] result of this: \n {} is this: \n {}'.format(str(ordered_dict).encode('utf8'), res))
    # err_logger.info('[CACHE] result is: {}'.format(res))
    return res


def send_sms_template(receiver, tokens=[], sms_type='verify_number'):
    if sms_type not in SMS_TEMPLATES:
        raise Exception('Invalid sms template')

    try:
        api = KavenegarAPI(settings.KAVEHNEGAR_API)
        params = {
            'receptor': receiver,
            'template': SMS_TEMPLATES[sms_type],
            'token': tokens[0],
            'type': 'sms',  # sms vs call
        }
        for i in range(1, len(tokens)):
            params['token{}'.format(i+1)] = tokens[i]

        response = api.verify_lookup(params)
        # print(response)

    except APIException as e:
        raise Exception(str(e))
    except HTTPException as e:
        raise Exception(str(e))


def send_request(url, method='GET', data=None, headers=None):
    """
    Sends a request using `requests` module.
    :param url: URL to send request to
    :param method: HTTP method to use e.g. GET, PUT, DELETE, POST
    :param data: Data to send in case of PUT and POST
    :param headers: HTTP headers to use
    :return: Returns a HTTP Response object
    """
    assert url and method
    assert method in ['GET', 'PUT', 'DELETE', 'POST']
    method = getattr(requests, method.lower())
    try:
        response = method(url=url, data=data, headers=headers)
        # fcm_logger.info(
        #     '[SEND_REQUEST] {} url: {} response: {} header: {} data: {}'.format(
        #         timezone.now(),
        #         url,
        #         response,
        #         headers,
        #         data
        #     )
        # )
    except Exception as e:
        pass
        # fcm_logger.info('[SEND_REQUEST] ERRORRR {}'.format(str(e)))

    return response


def send_onesignal_notification(msg, notif_title, target_device_keys, expire_after_hours, notif_data={}):
    notification_params = {}
    notification_params['app_id'] = settings.ONE_SIGNAL_APP_ID
    notification_params['contents'] = {"en": msg}
    notification_params['headings'] = {"en": notif_title}
    notification_params['include_player_ids'] = target_device_keys
    if expire_after_hours > 0:
        notification_params['ttl'] = int(expire_after_hours * 3600)

    if len(notif_data):
        notif_data['time_stamp'] = datetime.now().strftime('%Y-%m-%dT%H:%M%S'),
        notif_data['time_stamp_ms'] = int(datetime.now().timestamp())
        notification_params['data'] = notif_data

    notification_params = json.dumps(notification_params)
    headers = {'Content-Type': 'application/json'}
    api_url = "https://onesignal.com/api/v1/notifications"

    try_notif = 0
    notif_sent = 0

    while ((not notif_sent) and (try_notif < 2)):
        response = send_request(api_url, method='POST', headers=headers, data=notification_params)
        # print(response.content)
        # import pdb
        # pdb.set_trace()
        if response.ok:
            notif_sent = 1
        else:
            try_notif = try_notif + 1

    return notif_sent


def send_zoho_email(dst_addr, subject, content):
    url = 'https://mail.zoho.com/api/accounts/{}/messages'.format(settings.ZOHO_ACCOUNT_ID)
    headers = {
        'Authorization': settings.ZOHO_AUTH_TOKEN,
        'Content-Type': 'application/json'
    }
    body = {
        "fromAddress": "info@canto-app.ir",
        "toAddress": dst_addr,
        "subject": subject,
        "content": content
    }
    import json
    response = send_request(url=url, method='POST', data=json.dumps(body), headers=headers)
