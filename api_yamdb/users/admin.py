from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


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
