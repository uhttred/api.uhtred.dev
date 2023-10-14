from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from uhtred.insight.models import Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):

    list_display_links = ('name', )
    list_display = (
        'id',
        'name',
        'pt_name',
        'is_category',
        'is_main',
        'created_at')

    date_hierarchy = 'created_at'
    ordering = ('is_category', 'name', 'created_at')
    search_fields = ('name', 'pt_name')

    list_filter = (
        'is_category',
        'is_main')

    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'slug')}),
        (_('Details'), {
            'fields': (
                'name',
                'pt_name')}),
        (_('State and Date'), {
            'fields': (
                'is_category',
                'is_main',
                'created_at',
                'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'slug',
        'created_at',
        'updated_at')
