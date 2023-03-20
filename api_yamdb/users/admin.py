from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )
    list_editable = ('role',)
    list_filter = ('username', 'role',)
    search_fields = ('username', 'role',)


admin.site.register(User, UserAdmin)
