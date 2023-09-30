from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from split.views import UserCreate,UserListView,ExpenseListView,UserPassbookView,UserBalacesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User-related URLs
    path('api/users/register/', UserCreate.as_view(), name='user-registration'),
    path('api/user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/', UserListView.as_view(), name='user-list'),

    # Expense-related URLs
    path('api/expenses/', ExpenseListView.as_view(), name='expense-list'),

    # User balance and passbook URLs
    path('api/user_balances/', UserBalacesView.as_view(), name='user-balances'),
    path('api/passbook/', UserPassbookView.as_view(), name='user-passbook'),
]
