from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from uhtred.base.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):

    list_display_links = ('id', 'image', 'name', )
    list_display = (
        'id',
        'image',
        'name',
        'company_name',
        'headline',
        'created_at')
    
    date_hierarchy = 'created_at'
    ordering = ('name', 'created_at' )
    search_fields = ('name', 'job_title')

    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'name')}),
        (_('Details'), {
            'fields': (
                'headline',
                'job_title',
                'company_name',
                'website',
                'avatar',
                'image')}),
        (_('State and Date'), {
            'fields': ('created_at', 'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'created_at',
        'image',
        'updated_at')
    
    def image(self, obj):
        if obj.avatar:
            return obj.avatar.admin_image_preview()
        return '-'
    