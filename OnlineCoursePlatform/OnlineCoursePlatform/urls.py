
from django.contrib import admin
from django.urls import path
from view import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('home/', views.home), # welcome page
    path('signup/', views.sign_up),
    path('login/', views.login),
    path('check-login/', views.check_login),
    path('check-signup/', views.check_signup),
    path('update-account/', views.update_account),
    path('delete-account/', views.delete_account),
    path('help/', views.help),
    path('mycourses/', views.mycourses),
    path('course/', views.course ),
    path('get-data/', views.get_data)
]
