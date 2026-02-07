from rest_framework import serializers
from books.models import Book, Author



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'category', 'is_available', 'author', 'created_at', 'updated_at']


class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn']



class AuthorSerializer(serializers.ModelSerializer):
    books = SimpleBookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'books']

from rest_framework import serializers


class BorrowActionSerializer(serializers.Serializer):
    pass
