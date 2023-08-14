from uhtred.base.models import Image, Tag, Person, Quote
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
        fields = ['id', 'name', 'headline', 'job_title', 'company_name', 'website', 'avatar']
    
    avatar = ImageDetail(read_only=True)


class QuoteDetail(DynamicFieldsModelSerializer): 
    class Meta:
        model = Quote
        exclude = ['is_active']
    
    author = PersonDetail(read_only=True)
    brand_logo = ImageDetail(read_only=True)
    brand_logo_dark = ImageDetail(read_only=True)
