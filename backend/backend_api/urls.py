from django.urls import path
from backend_api.app_routes import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('make_transaction/', views.make_transaction, name='make_transaction'),
]