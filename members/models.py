from django.db import models
from users.models import User
from books.models import Book
# Create your models here.


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    membership_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Member"
    

class BorrowedBook(models.Model):
    BORROWED = 'Borrowed'
    RETURNED = 'Returned'

    STATUS_CHOICES = [
        (BORROWED, 'Borrowed'),
        (RETURNED, 'Returned'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_instances')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrowed_books')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=BORROWED)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.member.user.first_name} {self.member.user.last_name}"