from rest_framework import serializers

from uhtred.core.serializers import DynamicFieldsModelSerializer
from uhtred.notify.models import Email
from uhtred.insight.models import Topic


class EmailDetail(DynamicFieldsModelSerializer):

    class Meta:
        model = Email
        fields = '__all__'

    def create(self, data):

        email = Email.objects.create(
            name=data.get('name'),
            email=data.get('email').lower(),
            subscribe_to_all=data.get('subscribe_to_all', False))

        if subscribed_topics := data.get('subscribed_topics'):
            email.subscribed_topics.set(subscribed_topics)
        else:
            email.subscribed_topics.set(
                Topic.objects.filter(is_category=True))

        return email

