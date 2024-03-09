from django.urls import path
from backend_api.reg_auth import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('delete_account/', views.delete_account, name='delete_account'),
]