from django.urls import path, include
from books.views import BookViewSet, AuthorViewSet
from members.views import MemberViewSet, BorrowedBookViewSet
from rest_framework_nested import routers



router = routers.DefaultRouter()
router.register('books', BookViewSet, basename='books')
router.register('authors', AuthorViewSet, basename='authors')
router.register('members', MemberViewSet, basename='members')
router.register('borrowed-books', BorrowedBookViewSet, basename='borrowed-books')



urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt'))
     
]