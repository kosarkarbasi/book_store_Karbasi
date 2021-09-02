from rest_framework import serializers
from .models import Book


class WineSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'category', 'description', 'inventory', 'price', 'discount', 'image', 'score')
