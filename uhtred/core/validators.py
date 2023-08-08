import re
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


uuid_regex: str = '[0-9a-f]{8}-?[0-9a-f]{4}-?4[0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}'
slug_regex: str = '[-a-z0-9_]+'
int_id_regex: str = '[0-9]+'


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^(?![0-9.])[A-z0-9.]{3,20}(?<![.])$'
    message = _(
        'Invalid username. '
        'Username must contain only letters, numbers and the characters ./-/_ . '
        'Length must be between 3 and 25 characters')
    flags = 0

    @classmethod
    def match(cls, string):
        return re.match(cls.regex,string)


@deconstructible
class NameValidator(validators.RegexValidator):
    
    regex   = r'^[A-Za-zÀ-Ÿ0-9. ]{1,40}$'
    message =  _(
        '1 to 40 characters maximum. '
        'It must contain only letters and / or numbers. ')

    @classmethod
    def match(cls, string):
        return re.match(cls.regex,string)


@deconstructible
class EmailValidator(validators.RegexValidator):

    # regex = r'^([A-z]+\.*[A-z0-9]*@[A-z]+\.+[A-z]+\.*[A-z]*)$'
    regex = r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,})+$'
    message =  _('Invalid email')

    @classmethod
    def match(cls, string):
        return re.match(cls.regex,string)


@deconstructible
class PhoneAOValidator(validators.RegexValidator):
    
    regex = r'^(?:(\+244|00244))?(9)(1|2|3|4|5|9)([\d]{7,7})$'
    default_replace = r'\2\3\4'
    message =  _('Invalid national number of angola')

    @classmethod
    def match(cls, string):
        return re.match(cls.regex, string)
    
    @classmethod
    def clean_number(cls, phone: str):
        return re.sub(cls.regex, cls.default_replace, phone)
    
    @classmethod
    def is_the_same(cls, phone1: str, phone2: str):
        return cls.clean_number(phone1) == cls.clean_number(phone2)


DefaultPhoneValidator = PhoneAOValidator

@deconstructible
class NoPoitSequenceValidator(validators.RegexValidator):
    
    regex = r'[.]{2,}'
    inverse_match = True
    message =  _('Must not contain sequence of dots')

    @classmethod
    def match(cls, string):
        return not re.match(cls.regex,string)


@deconstructible
class PasswordValidator(validators.RegexValidator):
    
    regex   = r'^(.){8,}$'
    message =  _(
        'Weak password. 8 characters minimum. '
        'Must contain at least one capital letter, one lower case and one number'
    )

    @classmethod
    def match(cls, string):
        return re.match(cls.regex,string)
     