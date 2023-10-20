from django.utils.translation import get_language

from uhtred.core.serializers import DynamicFieldsModelSerializer
from uhtred.notify.models import Email
from uhtred.insight.models import Topic


class EmailDetail(DynamicFieldsModelSerializer):

    class Meta:
        model = Email
        fields = '__all__'

    def update(self, instance: Email, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.preferred_language = validated_data.get('preferred_language', instance.preferred_language)
        instance.subscribe_to_all = validated_data.get('subscribe_to_all', instance.subscribe_to_all)

        if topics := validated_data.get('subscribed_topics'):
            instance.subscribed_topics.clear()
            for topic_id in topics:
                instance.subscribed_topics.add(topic_id)

        instance.save()
        return instance

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
