from uhtred.base.models import Image, Tag, Person
from uhtred.core.serializers import DynamicFieldsModelSerializer


class ImageDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = Image
        fields = ['url', 'thumbnail_url']


class TagDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'slug', 'name', 'pt_name']

class PersonDetail(DynamicFieldsModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'headline', 'job_title', 'website', 'avatar']
    
    avatar = ImageDetail(read_only=True)
