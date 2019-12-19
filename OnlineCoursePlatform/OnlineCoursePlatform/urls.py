
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
    path('course/(?P<course_id>[0-9]+)/(?P<is_bought>[0-1])', views.course, name="course"),
    path('mycourses/(?P<person_id>[0-9]+)', views.mycourses, name="mycourses"),
    path('buy-course/', views.buy_course)
]
