from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UA
from django.utils.translation import gettext_lazy as _

from uhtred.user.models import User


@admin.register(User)
class UserAdmin(UA):

    list_display_links = ('username', )
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_staff',
        'is_active',
        'created_at',
        'updated_at'
    )

    date_hierarchy = 'created_at'
    ordering = ('-created_at', )
    search_fields = ('id', 'name', 'username', 'email' )
    list_filter = (
        'role',
        'is_staff',
        'is_superuser',
        'is_active')
    
    collaborator_fieldsets = (
        (_('Identity'), {
            'fields': ('role', 'id', 'uid', 'username', 'person', 'password')}),
        (_('Contact'), {
            'fields': ('name', 'email')}),
        (_('Permissions'), {
            'fields': ('groups', 'user_permissions', 
                'is_active', 'is_staff', 'is_superuser')})
    )
    
    manager_fieldsets = (
        (_('Identity'), {
            'fields': ('role', 'id', 'uid', 'username', 'person')}),
        (_('Contact'), {
            'fields': ('name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active',)})
    )

    readonly_fields = (
        'uid',
        'id')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'role',
                'name',
                'username',
                'person',
                'password1',
                'password2'),
        }),
        (_('Status'), {
            'classes': ('wide',),
            'fields': (
                'is_staff',
                'is_superuser',
                'is_active'),
        })
    )
    
    def get_fieldsets(self, request, obj):
        if obj:
            if obj.role == User.Role.MANAGER:
                return self.manager_fieldsets
            return self.collaborator_fieldsets
        return self.add_fieldsets

    # def get_readonly_fields(self, request, obj=None):
    #     if obj: # editing an existing object
    #         if obj.role == User.Role.MANAGER and request.user.is_superuser:
    #             # editing manager by superuser
    #             return self.readonly_fields + ('role',)
    #         # editing customer
    #         return self.readonly_fields + ('is_staff', 'is_superuser',
    #             'user_permissions', 'groups', 'password', 'role')
    #     return self.readonly_fields
        
    def has_change_permission(self, request, obj = None, **kwargs):
        if obj:
            if obj.is_superuser and not request.user.is_superuser:
                return False
        return super().has_change_permission(request, obj=obj, **kwargs)

    def has_delete_permission(self, request, *args, **kwargs):
        return False
