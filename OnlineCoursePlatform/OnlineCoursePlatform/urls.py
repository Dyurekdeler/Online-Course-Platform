
from django.contrib import admin
from django.urls import path
from view import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('home/', views.home), # welcome page
    path('signup/', views.sign_up),
    path('login/', views.login, name="login"),
    path('check-login/', views.check_login),
    path('check-signup/', views.check_signup),
    path('update-account/', views.update_account),
    path('delete-account/', views.delete_account),
    path('help/', views.help),
    path('course/', views.course),
    path('mycourses/(?P<person_id>[0-9]+)', views.mycourses, name="mycourses"),

    path('get-data/', views.get_data)
]
