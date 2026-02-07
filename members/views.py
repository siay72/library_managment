from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from members.models import Member
from members.serializers import MemberSerializer
from members.models import BorrowedBook
from members.serializers import (
    BorrowedBookSerializer,
    BorrowBookSerializer,
    ReturnBookSerializer
)
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        member = self.get_object()
        if member.borrowed_books.exists():
            return Response(
                {"error": "Cannot delete a member with borrowed books."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)



class BorrowedBookViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        return BorrowedBook.objects.select_related('member', 'book').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BorrowBookSerializer   
        if self.request.method in ['PUT', 'PATCH']:
            return ReturnBookSerializer   
        return BorrowedBookSerializer

    def destroy(self, request, *args, **kwargs):
        borrowed_book = self.get_object()
        if borrowed_book.status == BorrowedBook.BORROWED:
            return Response(
                {"error": "Cannot delete a book that is still borrowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)
