from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from martor.widgets import AdminMartorWidget

from uhtred.case.models import Case

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget}}
