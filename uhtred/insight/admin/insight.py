from django.db import models
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from martor.widgets import AdminMartorWidget

from uhtred.insight.models import Insight


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget}}

    list_display_links = ('id', 'title', )
    list_display = (
        'id',
        'title',
        'is_active',
        'published_at',
        'created_at')
    
    date_hierarchy = 'created_at'
    ordering = ('title', 'created_at' )
    search_fields = ('title', 'pt_title', 'id' )
    # list_filter = ()
    
    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'slug',
                'author',
                'cover',
                'image')}),
        (_('English Details'), {
            'fields': (
                'title',
                'description',
                'content')}),
        (_('Portuguese Details'), {
            'fields': (
                'pt_title',
                'pt_description',
                'pt_content')}),
        (_('Additional'), {
            'fields': (
                'visualisations',
                'tags',)}),
        (_('State and Date'), {
            'fields': (
                'is_active',
                'published_at',
                'created_at',
                'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'slug',
        'visualisations',
        'published_at',
        'image',
        'created_at',
        'updated_at')
    
    def image(self, obj):
        if obj.cover:
            return mark_safe(f'<img src="{obj.cover.url}" style="max-width:600px;"/>')
        return '-'
