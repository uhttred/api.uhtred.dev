from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from dynamic_raw_id.admin import DynamicRawIDMixin

from uhtred.insight.models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin, DynamicRawIDMixin):

    list_display_links = ('name', )
    list_display = (
        'id',
        'image',
        'name',
        'username',
        'headline',
        'created_at')

    date_hierarchy = 'created_at'
    ordering = ('name', 'created_at')
    search_fields = ('name', 'id')
    raw_id_fields = (
        'avatar',)

    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'name',
                'pt_name',
                'username')}),
        (_('Details'), {
            'fields': (
                'headline',
                'avatar',
                'image')}),
        (_('Social Links'), {
            'fields': (
                'website',
                'instagram',
                'linkedin')}),
        (_('State and Date'), {
            'fields': (
                'created_at',
                'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'created_at',
        'image',
        'updated_at')

    def image(self, obj):
        if obj.avatar:
            return obj.avatar.admin_image_preview(60)
        return '-'
