from django.urls import path
from backend_api.app_routes import views

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('get_email/', views.get_email, name='get_email'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('make_transaction/', views.make_transaction, name='make_transaction'),
    path('reset_request/', views.reset_request, name='reset_request'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('update_username/', views.update_username, name='update_username'),
    path('update_email/', views.update_email, name='update_email'),
    path('get_transaction_history/', views.get_transaction_history, name='get_transaction_history'),
    path('process_transaction_log/', views.process_transaction_log, name='process_transaction_log'),
    path('get_transaction_by_field/', views.get_transaction_by_field, name='get_transaction_by_field')
]
