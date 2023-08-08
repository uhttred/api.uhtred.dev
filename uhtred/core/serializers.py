from typing import Union
from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None,
            exclude: Union[list, tuple] = [],
            fields: Union[list, tuple] = [], **kwargs):
        super(DynamicFieldsModelSerializer, self).__init__(
            instance=instance, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for key in existing - allowed:
                self.fields.pop(key)
        elif exclude:
            existing = set(self.fields.keys())
            for key in exclude:
                if key in existing:
                    self.fields.pop(key)
