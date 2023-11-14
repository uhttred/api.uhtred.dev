# from django.utils.translation import gettext_lazy as _

from uhtred.store.models import Product
from uhtred.base.serializers import ImageDetail
from uhtred.core.serializers import DynamicFieldsModelSerializer


class ProductDetail(DynamicFieldsModelSerializer):

    class Meta:
        model = Product
        exclude = ['is_active']

    cover = ImageDetail(read_only=True)
