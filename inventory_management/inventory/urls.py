from django.urls import path
from .views import UserSignUp, UserLogin, ItemListCreate, ItemDetail

urlpatterns = [
    path('api/users/signup/', UserSignUp.as_view(), name='user-signup'),
    path('api/users/login/', UserLogin.as_view(), name='user-login'),
    path('api/items/', ItemListCreate.as_view(), name='item-list-create'),
   path('api/items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),

]
