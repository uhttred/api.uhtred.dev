from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from martor.widgets import AdminMartorWidget

from uhtred.case.models import Case


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget}}

    list_display_links = ('id', 'title', )
    list_display = (
        'id',
        'title',
        'is_active',
        'created_at')
    
    date_hierarchy = 'created_at'
    ordering = ('title', 'created_at' )
    search_fields = ('title', 'pt_title', 'id' )
    list_filter = (
        'is_active',)
    
    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'slug',)}),
        (_('Basic Details'), {
            'fields': (
                'year',
                'title',
                'description',
                'pt_title',
                'pt_description')}),
        (_('Images'), {
            'fields': (
                'cover',
                'cover_preview',
                'banner',
                'banner_preview',
                'banner_dark',
                'banner_dark_preview',
                'brand_logo',
                'brand_logo_preview',
                'brand_logo_dark',
                'brand_logo_dark_preview')}),
        (_('English Content'), {
            'fields': (
                'content',)}),
        (_('Portuguese Content'), {
            'fields': (
                'pt_content',)}),
        (_('Additional Data'), {
            'fields': (
                'data',)}),
        (_('State and Date'), {
            'fields': ('is_active', 'created_at', 'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'slug',
        'cover_preview',
        'banner_preview',
        'banner_dark_preview',
        'brand_logo_preview',
        'brand_logo_dark_preview',
        'created_at',
        'updated_at')
    
    def cover_preview(self, obj):
        if obj.cover:
            return obj.cover.admin_image_preview()
        return '-'
    
    def banner_preview(self, obj):
        if obj.banner:
            return obj.banner.admin_image_preview()
        return '-'
    
    def banner_dark_preview(self, obj):
        if obj.banner_dark:
            return obj.banner_dark.admin_image_preview()
        return '-'
    
    def brand_logo_preview(self, obj):
        if obj.brand_logo_dark:
            return obj.brand_logo.admin_image_preview()
        return '-'
    
    def brand_logo_dark_preview(self, obj):
        if obj.brand_logo_dark:
            return obj.brand_logo_dark.admin_image_preview()
        return '-'
