# -*- coding: utf-8 -*-


class ErrorMessaging:
    ERRORS = {
        'farsi': {
            'Invalid_Birth_Date': ' تاریخ تولد مشخص‌شده معتبر نیست',
            'Missing_Birth_Date': ' تاریخ تولد مشخص نشده است',
            'Invalid_Mobile': u'شماره موبایل باید ۱۱ رقم داشته باشد و با ۰۹ شروع شود',
            'Missing_Mobile': u' شماره تلفن همراهی وارد نشده است',
            'Invalid_Age': u' تاریخ تولد مشخص‌شده معتبر نیست',
            'Missing_Age': u' تاریخ تولد مشخص نشده است',
            'Invalid_Email': u' ایمیل باید در قالب xxxxxxx@xxx.xx باشد.',
            'Missing_Email': u' ایمیلی وارد نشده است',
            'Invalid_Gender': u'جنسیت مشخص‌شده معتبر نیست',
            'Missing_Gender': u'جنسیتی مشخص نشده است',
            'Invalid_Udid': u' UDID معتبر نیست ',
            'Missing_Udid': u' UDID مشخص نشده است ',
            'Invalid_Os_Version': u'نسخه سیستم عامل دستگاه با برنامه همخوانی ندارد',
            'Missing_Os_Version': u'نسخه سیستم عامل دستگاه در دسترس نیست',
            'Invalid_Type': u'نوع سیستم عامل دستگاه با برنامه همخوانی ندارد',
            'Missing_Type': u'نوع سیستم عامل دستگاه ناشناخته است',
            'Invalid_Username': u'نام کاربری باید تنها شامل حروف انگلیسی، اعداد انگلیسی، "_" و "-" باشد',
            'Missing_Username': u'نام کاربری وارد نشده است',
            'Username_Exists': u' نام کاربری وارد شده در سرور وجود دارد',
            'User_Not_Found': u'کاربری با مشخصات داده شده یافت نشد',
            'Invalid_Country': u'نام کشور وارد شده اشتباه است',
            'Missing_Country': u'نام کشور وارد نشده است',
            'Invalid_Password': u'رمز وارد شده صحیح نمی باشد',
            'Missing_Password': u'رمز ورود وارد نشده است',
            'Invalid_Login': u'نام کاربری یا رمز کاربری وارد شده معتبر نمی باشد.',
            'Invalid_Referrer': u' تاریخ تولد مشخص‌شده معتبر نیست',
            'Missing_Referrer': u' تاریخ تولد مشخص نشده است',
            'Missing_Form': u'حداقل یکی از موارد را ارسال کنید'
        },
        'eng': {
            'Invalid_Birth_Date': ' The set birthday is invalid.',
            'Missing_Birth_Date': ' No birthday has been set.',
            'Invalid_Mobile': ' Mobile phone number should contain 11 digits and start with 09.',
            'Missing_Mobile': ' No mobile phone number has been entered.',
            'Invalid_Age': ' The set birthday is invalid.',
            'Missing_Age': ' No birthday has been set.',
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
            'Username_Exists': 'Username already exists.',
            'User_Not_Found': 'No user found with given info',
            'Invalid_Country': '',
            'Missing_Country': '',
            'Invalid_Password': 'Password is wrong or invalid pattern',
            'Missing_Password': 'Password is empty',
            'Invalid_Login': 'Username or Password is not correct',
            'Invalid_Referrer': 'Referrer is wrong or invalid pattern',
            'Missing_Referrer': 'Referrer is empty',
            'Missing_Form': 'At least fill one of the inputs'

        }
    }
    LANGUAGE_FARSI = 'farsi'
    LANGUAGE_ENGLISH = 'eng'
    LANGUAGES = [LANGUAGE_FARSI, LANGUAGE_ENGLISH]

    def get_error_data(self, error_key=None):
        if not error_key:
            return {}
        return {x: self.ERRORS[x][error_key] for x in self.ERRORS}

    @staticmethod
    def get_errors(self, error_list=None, language=LANGUAGE_FARSI):
        if error_list is None:
            error_list = []
        return [{'error': self.ERRORS[language][x]} for x in error_list]
