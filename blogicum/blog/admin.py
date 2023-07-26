from django.contrib import admin

from blog.models import Post, Category, Location, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'location',
        'is_published',
        'category'
    )
    list_editable = (
        'is_published',
        'category'
    )
    search_fields = ('text',)
    list_filter = ('is_published',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Comment)
