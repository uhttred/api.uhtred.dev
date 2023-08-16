from django import forms
from django.contrib import admin
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
    
    def thumbnail_preview(self, obj: Image):
        return obj.admin_thumbnail_preview()

    def file_preview(self, obj: Image):
        return obj.admin_image_preview()
    
    def image(self, obj):
        return obj.admin_thumbnail_preview(80)
