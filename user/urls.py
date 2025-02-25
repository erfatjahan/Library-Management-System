from django.urls import path
from user.views import BuyBookView, RegistrationView, ReturnBookView, UserLoginView
from . import views
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('add_money/', views.add_money, name='add_money'),
    path('buy_book/<int:book_id>/', BuyBookView.as_view(), name='buy_book'),
    path('profile/', views.profile_view, name='profile'),
    path('return_book/<int:book_id>/', ReturnBookView.as_view(), name='return_book'),
]
