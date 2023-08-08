from django.contrib import admin

from uhtred.base.models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
