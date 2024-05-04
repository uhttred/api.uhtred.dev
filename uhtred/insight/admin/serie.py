from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from dynamic_raw_id.admin import DynamicRawIDMixin

from uhtred.user.models import User
from uhtred.insight.models import Serie, SerieItem


class SerieItemInline(admin.TabularInline, DynamicRawIDMixin):
    model = SerieItem
    raw_id_fields = (
        'insight',)
    extra = 1


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin, DynamicRawIDMixin):

    inlines = [SerieItemInline]

    list_display_links = ('title', )
    list_display = (
        'id',
        'title',
        'status',
        'is_active',
        'created_at')

    date_hierarchy = 'created_at'
    ordering = ('title', )
    search_fields = ('title', 'pt_title', 'id')

    filter_horizontal = ('topics', )
    list_filter = (
        'status',
        'is_active',)

    fieldsets = (
        (_('Identity'), {
            'fields': (
                'id',
                'uid',
                'slug',
                'created_by',
                'author'
            )}),
        (_('English Details'), {
            'fields': (
                'title',
                'description')}),
        (_('Portuguese Details'), {
            'fields': (
                'pt_title',
                'pt_description')}),
        (_('Additional'), {
            'fields': (
                'topics',)}),
        (_('State and Date'), {
            'fields': (
                'status',
                'is_active',
                'created_at',
                'updated_at')})
    )

    readonly_fields = (
        'id',
        'uid',
        'slug',
        'created_at',
        'updated_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'created_by':
            kwargs['queryset'] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
