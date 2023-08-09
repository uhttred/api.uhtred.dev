from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django_svg_image_form_field import SvgAndImageFormField

from uhtred.base.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        exclude = []
        field_classes = {
            'file': SvgAndImageFormField,
        }


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    
    form = ImageForm
    list_display_links = ('id', 'image', 'name', )
    list_display = (
        'id',
        'image',
        'name',
        'created_at')
    
    date_hierarchy = 'created_at'
    ordering = ('name', 'created_at' )
    search_fields = ('name',)

    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'name')}),
        (_('Files'), {
            'fields': (
                'file',
                'file_preview',
                'thumbnail_preview')}),
        (_('State and Date'), {
            'fields': ('created_at', 'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'thumbnail_preview',
        'created_at',
        'updated_at',
        'image',
        'file_preview')
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail_url}" style="max-width:300px;"/>')
        return '-'

    def file_preview(self, obj):
        return mark_safe(f'<img src="{obj.url}" style="max-width:300px;"/>')
    
    def image(self, obj):
        return mark_safe(f'<img src="{obj.url}" style="max-width:80px;"/>')
