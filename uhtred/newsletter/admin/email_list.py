from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from uhtred.newsletter.models import EmailList


@admin.register(EmailList)
class EmailListAdmin(admin.ModelAdmin):

    list_display_links = ('id', 'email', )
    list_display = (
        'id',
        'email',
        'name',
        'verified',
        'is_active',
        'created_at')
    
    date_hierarchy = 'created_at'
    ordering = ('email', 'created_at' )
    search_fields = ('email', 'name', 'id')
    list_filter = (
        'is_active',
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
                'tags')}),
        (_('State and Date'), {
            'fields': (
                'is_active',
                'verified',
                'created_at',
                'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'created_at',
        'updated_at')
    