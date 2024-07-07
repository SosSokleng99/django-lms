from django.urls import path
from . import views

urlpatterns = [
    #Read Data from Model
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),


    #Create URL PATH for Listing User's Borrowed Book
    path('my-books/', views.LoanedBooksByUserListView.as_view(), name='my-books'),

    #Create URL Path for Listing All Borrowed Book for Superuser
    path('all-borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),

    #Create URL Path for Update Due Date Book
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),

    #Author: Create, Update and Delete Data URL Path
    path('author/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
]