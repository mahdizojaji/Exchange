from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as _UserAdmin


@admin.register(get_user_model())
class UserAdmin(_UserAdmin):
    fieldsets = (
        (None, {"fields": ('uuid', 'created_at', 'updated_at')}),
        *_UserAdmin.fieldsets,
    )
    add_fieldsets = (
        (None, {"fields": ('uuid', 'created_at', 'updated_at')}),
        *_UserAdmin.add_fieldsets,
    )
    readonly_fields = (
        'uuid',
        'created_at',
        'updated_at',
        *_UserAdmin.readonly_fields,
    )
