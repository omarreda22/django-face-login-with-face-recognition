from django.urls import path

from . import views

app_name = 'accounts'


urlpatterns = [
    path('', views.accounts_home, name='home'),
    path('register/', views.accounts_register, name='register'),
    path('login/', views.accounts_login_page, name="login"),
    path("login_face/", views.accounts_login, name="login_face"),
    path("logout/", views.accounts_logout, name="logout"),
]
