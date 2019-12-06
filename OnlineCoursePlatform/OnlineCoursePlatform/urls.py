
from django.contrib import admin
from django.urls import path
from view import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.index),
    path('signup/', views.sign_up),
    path('login/', views.check_login),
    path('check-signup/', views.check_signup),
    path('update-account/', views.update_account),
    path('delete-account/', views.delete_account),
    path('', views.index)
]
