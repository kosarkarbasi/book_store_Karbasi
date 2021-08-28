from django.contrib import admin, messages
from django.db.models import F

from .models import Book, Author, Category, Comment

# Register your models here.
# admin.site.register(Comment)
admin.site.register(Category)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Book)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("title", 'price', 'discount', 'inventory')
    list_editable = ['inventory']
    # prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created', ]
    actions = ['add_inventory', ]

    def add_inventory(self, request, queryset):
        """
        add 2 inventory to selected items
        """
        updated = queryset.update(inventory=F('inventory') + 2)
        self.message_user(request, '2 more inventory added to selected books', messages.SUCCESS)

    add_inventory.short_description = 'Add two inventory to selected books'

    fieldsets = (
        ('Public information', {
            'fields': ('title', 'description', 'price', 'discount', 'inventory', 'image', 'score', 'created',)
        }),

        ('Details', {
            'classes': ('collapse',),
            'fields': ('author', 'category')
        })
    )
