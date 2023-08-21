from typing import Any, Optional
from django.db import models
from django.contrib import admin, messages
from django.db.models.fields import Field
from django.forms.fields import TypedChoiceField
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect

from martor.widgets import AdminMartorWidget

from uhtred.user.models import User
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
        'is_completed',
        'published_at',
        'created_at')
    
    date_hierarchy = 'created_at'
    ordering = ('title', 'created_at' )
    search_fields = ('title', 'pt_title', 'id' )
    list_filter = (
        'published_at',
        'is_active',
        'is_completed')
    
    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'slug',
                'created_by',
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
                'is_completed',
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
    
    change_form_template = 'insight/admin/change_insight_form.html'
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.created_by:
            return self.readonly_fields + ('created_by', )
        return self.readonly_fields
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'created_by':
            kwargs['queryset'] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def image(self, obj):
        if obj.cover:
            return obj.cover.admin_image_preview()
        return '-'
    
    def has_delete_permission(self, request: HttpRequest, obj = None) -> bool:
        if obj and request.user.role == User.Role.COLLABORATOR:
            if obj.created_by == request.user or obj.author == request.user.person:
                return True
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self, request: HttpRequest, obj = None) -> bool:
        if obj and request.user.role == User.Role.COLLABORATOR:
            if obj.created_by == request.user or obj.author == request.user.person:
                return True
        return super().has_delete_permission(request, obj)
    
    def publish_insight(self, request, insight: Insight) -> None:
        if insight.publish():
            return self.message_user(request,
                                     _('Article published'))
        return self.message_user(
            request,
            _('Unpublished article. Incomplete or already published article.'),
            messages.ERROR)
    
    def response_change(self, request, obj: Insight):
        if '_publish' in request.POST:
            self.publish_insight(request, obj)
            return HttpResponseRedirect('.')
        return super().response_change(request, obj)
