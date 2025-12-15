from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

app_name = 'api'

urlpatterns = [
    path('books/update/', BookUpdateView.as_view(), name='book-update-no-pk'),
    path('books/delete/', BookDeleteView.as_view(), name='book-delete-no-pk'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]