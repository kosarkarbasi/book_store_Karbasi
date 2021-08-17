from django.contrib import admin
from .models import Book, Author, Category, Comment

# Register your models here.
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)


@admin.register(Book)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("title", 'price', 'discount', 'slug')
    prepopulated_fields = {'slug': ('title',)}

