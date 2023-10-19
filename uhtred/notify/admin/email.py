from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# from dynamic_raw_id.admin import DynamicRawIDMixin
# from dynamic_raw_id.filters import DynamicRawIDFilter

from uhtred.notify.models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display_links = ('email',)
    list_display = (
        'id',
        'email',
        'name',
        'preferred_language',
        'verified',
        'subscribe_to_all',
        'created_at')

    date_hierarchy = 'created_at'
    ordering = ('name', 'email')
    filter_horizontal = ('subscribed_topics',)
    search_fields = ('email', 'name', 'id')
    list_filter = (
        'preferred_language',
        'subscribe_to_all',
        'verified')

    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'email')}),
        (_('Mode Detail'), {
            'fields': (
                'name',
                'preferred_language',
                'subscribed_topics')}),
        (_('State and Date'), {
            'fields': (
                'verified',
                'subscribe_to_all',
                'created_at',
                'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'created_at',
        'updated_at')
