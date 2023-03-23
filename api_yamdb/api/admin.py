from django.contrib import admin

from reviews.models import Category, Genre, Titles, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = ('title', )


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Titles)
admin.site.register(Review)
admin.site.register(Comment)
