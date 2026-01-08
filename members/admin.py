from django.contrib import admin
from .models import Member, BorrowedBook
# Register your models here.


admin.site.register(Member)
admin.site.register(BorrowedBook)