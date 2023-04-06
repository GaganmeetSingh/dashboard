from django.urls import path
from dashboard_app import views

app_name = 'dashboard_app'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('update/<int:id>', views.update, name='update'),
    path('update/', views.update, name='update'),
    path('fetch_users/', views.get_all_users, name='fetch_users'),
    path('reset_password/<int:id>/', views.reset_password, name='reset_password'),
]