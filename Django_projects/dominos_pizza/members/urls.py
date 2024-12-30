from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('accounts/emailsignup/', views.register, name ='register'),
    path('posts/', views.show_posts, name='posts'),
    path('login/',views.login_view,name="login"),
]

