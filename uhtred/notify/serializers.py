from django.utils.translation import get_language

from uhtred.core.serializers import DynamicFieldsModelSerializer
from uhtred.notify.models import Email
from uhtred.insight.models import Topic


class EmailDetail(DynamicFieldsModelSerializer):

    class Meta:
        model = Email
        fields = '__all__'

    def create(self, data):

        language = get_language()[:2]
        language = language if language in ['pt', 'en'] else None

        email = Email.objects.create(
            name=data.get('name'),
            email=data.get('email').lower(),
            preferred_language=data.get('preferred_language', language),
            subscribe_to_all=data.get('subscribe_to_all', False))

        if subscribed_topics := data.get('subscribed_topics'):
            email.subscribed_topics.set(subscribed_topics)
        else:
            email.subscribed_topics.set(
                Topic.objects.filter(is_category=True))

        return email
