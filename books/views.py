from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from books.models import Book, Author
from rest_framework.response import Response
from rest_framework import status
from members.models import BorrowedBook
from books.serializers import BookSerializer , AuthorSerializer, BorrowActionSerializer
from api.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class BookViewSet(ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'category', 'isbn']
    ordering_fields = ['created_at', 'updated_at', 'title']

    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        if BorrowedBook.objects.filter(book=book).exists():
            return Response(
                {"error": "This book is currently borrowed and cannot be deleted."},
                  status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
    
    
    @action(
    detail=True,
    methods=['post'],
    permission_classes=[IsAuthenticated],
    serializer_class=BorrowActionSerializer
    )
    def borrow(self, request, pk=None):

        book = self.get_object()

        if not book.is_available:
            return Response(
            {"error": "This book is already borrowed."},
            status=status.HTTP_400_BAD_REQUEST
        )

        try:
            member = request.user.member_profile
        except:
            return Response(
            {"error": "You must be a library member to borrow books."},
            status=status.HTTP_400_BAD_REQUEST
        )

        borrowed = BorrowedBook.objects.create(
            book=book,
            member=member,
            borrow_date=status.HTTP_201_CREATED
        )

        book.is_available = False
        book.save()

        return Response({
            "message": f"You have successfully borrowed '{book.title}'",
            "borrow_id": borrowed.id,
            "book_id": book.id,
            "member_id": member.id,
            "member_email": member.user.email,
            "member_name": f"{member.user.first_name} {member.user.last_name}",
            "borrowed_at": borrowed.borrow_date
        }, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(
        operation_summary='Retrive a list of books'
    )
    def list(self, request, *args, **kwargs):
        """Retrive all the book"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a Book by admin",
        operation_description="This allow an admin to create a Book",
        request_body=BookSerializer,
        responses={
            201: BookSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create Book"""
        return super().create(request, *args, **kwargs)
    




class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]    