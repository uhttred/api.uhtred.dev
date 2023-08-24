from uhtred.newsletter.models import EmailList

from uhtred.core.serializers import (
    DynamicFieldsModelSerializer)


class EmailListDetail(DynamicFieldsModelSerializer):
    
    class Meta:
        model = EmailList
        exclude = ['is_active']
    
    def create(self, validated_data):
        return EmailList.objects.create(
            email=validated_data.get('email').lower(),
            name=validated_data.get('name', ''))
