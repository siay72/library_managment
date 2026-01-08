from rest_framework import serializers
from members.models import BorrowedBook, Member
from books.models import Book



class MemberSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(
        source='user.email', read_only=True
    )

    class Meta:
        model = Member
        fields = [
            'id',
            'user',
            'user_email',
            'membership_date',
            'is_active'
        ]
        read_only_fields = ['membership_date']


class BorrowBookSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(write_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    member_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BorrowedBook
        fields = ['id', 'book_id','book_title', 'member_id', 'borrow_date', 'status']
        read_only_fields = ['borrow_date', 'status']

    def create(self, validated_data):
        book = Book.objects.get(id=validated_data['book_id'])
        member = Member.objects.get(id=validated_data['member_id'])

        book = Book.objects.get(id=validated_data['book_id'])
        if not book.is_available:
            raise serializers.ValidationError("This book is currently not available for borrowing.")
        
        member = Member.objects.get(id=validated_data['member_id'])

        book.is_available = False
        book.save()

        return BorrowedBook.objects.create(
            book=book,
            member=member
        )


class ReturnBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = ['return_date', 'status']



class BorrowedBookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    member_name = serializers.CharField(
        source='member.user.first_name', read_only=True
    )

    class Meta:
        model = BorrowedBook
        fields = [
            'id',
            'book',
            'book_title',
            'member',
            'member_name',
            'borrow_date',
            'return_date',
            'status'
        ]
