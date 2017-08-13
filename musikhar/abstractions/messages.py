# -*- coding: utf-8 -*-

ERRORS = {
    'farsi': {
        'Invalid_Mobile': 'شماره موبایل باید ۱۱ رقم داشته باشد و با ۰۹ شروع شود',
        'Missing_Mobile': ' شماره تلفن همراهی وارد نشده است',
        'Invalid_Birth_Date': ' تاریخ تولد مشخص‌شده معتبر نیست',
        'Invalid_Birth_Date': ' تاریخ تولد مشخص نشده است',
        'Invalid_Email': ' ایمیل باید در قالب xxxxxxx@xxx.xx باشد.',
        'Missing_Email': ' ایمیلی وارد نشده است',
        'Invalid_Gender': 'جنسیت مشخص‌شده معتبر نیست',
        'Missing_Gender': 'جنسیتی مشخص نشده است',
        'Invalid_Udid': ' UDID معتبر نیست ',
        'Missing_Udid': ' UDID مشخص نشده است ',
        'Invalid_Os_Version': 'نسخه سیستم عامل دستگاه با برنامه همخوانی ندارد',
        'Missing_Os_Version': 'نسخه سیستم عامل دستگاه در دسترس نیست',
        'Invalid_Type': 'نوع سیستم عامل دستگاه با برنامه همخوانی ندارد',
        'Missing_Type': 'نوع سیستم عامل دستگاه ناشناخته است',
        'Invalid_Username': 'نام کاربری باید تنها شامل حروف انگلیسی، اعداد انگلیسی، "_" و "-" باشد',
        'Missing_Username': 'نام کاربری وارد نشده است',
        'Invalid_Country':'',
        'Missing_Country':'',
    },
    'eng': {

        'Invalid_Mobile': ' Mobile phone number should contain 11 digits and start with 09.',
        'Missing_Mobile': ' No mobile phone number has been entered.',
        'Invalid_Birth_Date': ' The set birthday is invalid.',
        'Invalid_Birth_Date': ' No birthday has been set.',
        'Invalid_Email': ' E-mail should be structured as “xxxxxxx@xxx.xx”.',
        'Missing_Email': ' No E-mail has been set.',
        'Invalid_Gender': ' The set gender is invalid.',
        'Missing_Gender': 'No gender has been set.',
        'Invalid_Udid': 'The UDID is invalid.',
        'Missing_Udid': ' The UDID is missing.',
        'Invalid_Os_Version': 'The device’s OS version is incompatible with the app.',
        'Missing_Os_Version': 'The device’s OS version is unattainable.',
        'Invalid_Type': 'The device’s type is incompatible with the app.',
        'Missing_Type': 'The device’s type is unknown.',
        'Invalid_Username': 'Username should only contain letters, numbers, “_” and or “-“.',
        'Missing_Username': 'No username has been entered.',
        'Invalid_Country':'',
        'Missing_Country':'',

        
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
