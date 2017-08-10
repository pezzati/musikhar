# -*- coding: utf-8 -*-

ERRORS = {
    'farsi': {
        'Invalid_Mobile': u'شماره موبایل بایستی ۱۱ رقم و با ۰۹ شروع شود',
        'Invalid_Age': u'سن باید عددی بزرگتر از صفر باشد'
    },
    'eng': {
        'Invalid_Mobile': 'Mobile number must only be 11 integers and start with 09',
        'Invalid_Age': 'Age must be an integer greater than zero'
    }
}


class ErrorMessaging:
    @staticmethod
    def get_error_data(error_key=None):
        if not error_key:
            return {}
        # TODO handel the errors
        return {x: ERRORS[x][error_key] for x in ERRORS}

    def get_errors(self, error_list=None):
        if error_list is None:
            error_list = []
        return [self.get_error_data(x) for x in error_list]
