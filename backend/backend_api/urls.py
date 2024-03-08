from django.urls import path
from backend_api.reg_auth import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('delete_account/', views.delete_account, name='delete_account'),
]