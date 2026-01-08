from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from books.models import Book, Author
from rest_framework.response import Response
from rest_framework import status
from members.models import BorrowedBook
from books.serializers import BookSerializer , AuthorSerializer   
# Create your views here.


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
      
    def destroy(self, request, *args, **kwargs):
        book = self.get_object()

        if BorrowedBook.objects.filter(
            book=book,
            status=BorrowedBook.BORROWED
        ).exists():
            return Response(
                {"error": "Cannot delete a book that is currently borrowed."},
                status=status.HTTP_400_BAD_REQUEST
            )   

        return super().destroy(request, *args, **kwargs)



class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer