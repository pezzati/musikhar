# -*- coding: utf-8 -*-

ERRORS = {
    'farsi': {
        'Invalid_Mobile': u'شماره موبایل بایستی ۱۱ رقم و با ۰۹ شروع شود',
        'Missing_Mobile': '',
        'Invalid_Age': 'سن باید عددی بزرگتر از صفر باشد',
        'Missing_Age': '',
        'Invalid_Email': '',
        'Missing_Email': '',
        'Invalid_Gender': '',
        'Missing_Gender': '',
        'Invalid_Udid': 'Age must be an integer greater than zero',
        'Missing_Udid': '',
        'Invalid_Os_Version': '',
        'Missing_Os_Version': '',
        'Invalid_Type': '',
        'Missing_Type': '',
        'Invalid_Username': '',
        'Missing_Username': '',

    },
    'eng': {
        'Invalid_Mobile': 'Mobile number must only be 11 integers and start with 09',
        'Missing_Mobile': '',
        'Invalid_Age': 'Age must be an integer greater than zero',
        'Missing_Age': '',
        'Invalid_Email': '',
        'Missing_Email': '',
        'Invalid_Gender': '',
        'Missing_Gender': '',
        'Invalid_Udid': 'Age must be an integer greater than zero',
        'Missing_Udid': '',
        'Invalid_Os_Version': '',
        'Missing_Os_Version': '',
        'Invalid_Type': '',
        'Missing_Type': '',
        'Invalid_Username': '',
        'Missing_Username': '',
        
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
