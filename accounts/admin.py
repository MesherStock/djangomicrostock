from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


class UserAccountAdmin(UserAdmin):

    list_display = ('email','username', 'first_name', 'last_name','last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'username', 'first_name',)
    list_editable = ['is_active',]
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    readonly_fields = ['date_joined', 'last_login',]
    ordering = ('-date_joined',)

admin.site.register(User, UserAccountAdmin)
