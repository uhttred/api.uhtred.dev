from uhtred.base.models import Image, Tag
from uhtred.core.serializers import DynamicFieldsModelSerializer


class ImageDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = Image
        fields = ['url', 'thumbnail_url']


class TagDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'slug', 'name', 'pt_name']
