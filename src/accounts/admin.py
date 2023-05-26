from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import NewUser
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'first_name',
                    'last_name', 'is_admin', 'is_staff')
    list_filter = ('is_admin', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username',
                           'first_name', 'last_name', 'password')}),
        ('Email', {'fields': ('email',)}),
        ('Personal info', {'fields': ('country', 'gender', 'id_image', 'date_of_birth', 'phone_number')}),
        ('Permissions', {'fields': ('is_active',
                                    'is_admin', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'gender', 'id_image', 'country', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')


admin.site.register(NewUser, UserAdmin)