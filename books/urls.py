from django.urls import path
from .views import all_books, ShowDetails

urlpatterns = [
    path('all_books/', all_books, name='all_books'),
    path('details/<int:id>/', ShowDetails.as_view(), name='book_details'),
    path('comment/<int:id>/', ShowDetails.as_view(), name='comment_page'),
    path('category_wise_book/<slug:category_slug>/', all_books, name='category_wise_book'),
]
