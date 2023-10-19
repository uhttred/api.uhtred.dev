from django.conf import settings
from django.utils.translation import gettext_lazy as _

APP_CONFIGURATION_DICT_NAME: str = 'UHTRED'


class DictAsObject:
    defaults: dict

    def __init__(self, defaults: dict) -> None:
        self.defaults = defaults or dict()

    def __getattr__(self, attr: str):
        try:
            value = self.defaults[attr]
        except KeyError:
            raise AttributeError(_("Invalid key: '%s'") % attr)
        setattr(self, attr, value)
        return value


class AppConfigurations:
    __defaults: dict

    def __init__(self) -> None:
        self.__defaults = getattr(settings, APP_CONFIGURATION_DICT_NAME, {})

    def __getattr__(self, attr: str):
        try:
            value = self.__defaults[attr]
        except KeyError:
            raise AttributeError(
                _("Invalid {} setting: '{}'".format(APP_CONFIGURATION_DICT_NAME, attr)))
        finally:
            if isinstance(value, dict):
                value = DictAsObject(value)
        setattr(self, attr, value)
        return value


conf = AppConfigurations()
