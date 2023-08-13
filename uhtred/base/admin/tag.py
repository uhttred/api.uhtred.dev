from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from uhtred.base.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display_links = ('id', 'name', )
    list_display = (
        'id',
        'name',
        'pt_name',
        'created_at')
    
    date_hierarchy = 'created_at'
    ordering = ('name', 'created_at' )
    search_fields = ('name', 'pt_name')

    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'slug')}),
        (_('Details'), {
            'fields': (
                'name',
                'pt_name',
                'description')}),
        (_('State and Date'), {
            'fields': ('created_at', 'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'slug',
        'created_at',
        'updated_at')
    