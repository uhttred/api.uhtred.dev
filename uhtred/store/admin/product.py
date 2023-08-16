from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from uhtred.store.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display_links = ('id', 'name', )
    list_display = (
        'id',
        'name',
        'created_at',
        'updated_at')
    
    date_hierarchy = 'created_at'
    ordering = ('name', 'created_at' )
    search_fields = ('name', )

    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'slug',
                'name')}),
        (_('Details'), {
            'fields': (
                'buy_at',
                'price',
                'cover',
                'image')}),
        (_('Details'), {
            'fields': (
                'tags',)}),
        (_('State and Date'), {
            'fields': (
                'is_active',
                'created_at',
                'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'slug',
        'created_at',
        'image',
        'updated_at')
    
    def image(self, obj):
        if obj.cover:
            return obj.cover.admin_image_preview()
        return '-'
    