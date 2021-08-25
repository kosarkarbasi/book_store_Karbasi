from django.contrib import admin, messages
from django.db.models import F

from .models import Book, Author, Category, Comment

# Register your models here.
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)


@admin.register(Book)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("title", 'price', 'discount', 'slug')
    # prepopulated_fields = {'slug': ('title',)}

    actions = ['add_inventory', ]

    def add_inventory(self, request, queryset):
        updated = queryset.update(inventory=F('inventory') + 2)
        self.message_user(request, '2 more inventory added to selected books', messages.SUCCESS)

    add_inventory.short_description = 'Add two inventory to selected books'

    fieldsets = (
        ('Public information', {
            'fields': ('title', 'price', 'discount', 'inventory')
        }),

        ('Details', {
            'classes': ('collapse',),
            'fields': ('author', 'category')
        })
    )
