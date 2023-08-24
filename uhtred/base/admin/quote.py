from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from uhtred.base.models import Quote

from dynamic_raw_id.admin import DynamicRawIDMixin



@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin, DynamicRawIDMixin):

    list_display_links = ('id', 'author_name')
    list_display = (
        'id',
        'author_name',
        'is_active',
        'created_at',
        'updated_at')
    
    date_hierarchy = 'created_at'
    ordering = ('author__name', 'created_at' )
    search_fields = ('author__name',)
    raw_id_fields = (
        'brand_logo',
        'brand_logo_dark')

    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'author')}),
        (_('Details'), {
            'fields': (
                'text',
                'pt_text')}),
        (_('Brand'), {
            'fields': (
                'brand_logo',
                'brand_logo_preview',
                'brand_logo_dark',
                'brand_logo_dark_preview')}),
        (_('State and Date'), {
            'fields': (
                'is_active',
                'created_at',
                'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'author_name',
        'brand_logo_dark_preview',
        'created_at',
        'updated_at',
        'brand_logo_preview')
    
    def brand_logo_preview(self, obj):
        if obj.brand_logo:
            return obj.brand_logo.admin_image_preview()
        return '-'
    
    def brand_logo_dark_preview(self, obj):
        if obj.brand_logo_dark:
            return obj.brand_logo_dark.admin_image_preview()
        return '-'
