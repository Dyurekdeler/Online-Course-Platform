
from django.contrib import admin
from django.urls import path
from view import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('admin/', views.admin),
    path('', views.home, name="logout"), # welcome page
    path('home/(?P<person_id>[0-9]+)', views.home_user, name="home"),
    path('signup/(?P<person_id>[0-9]+)', views.sign_up, name="signup"),
    path('login/(?P<person_id>[0-9]+)', views.login, name="login"),
    path('check-login/', views.check_login),
    path('check-signup/', views.check_signup),
    path('update-account/(?P<person_id>[0-9]+)', views.update_account, name="update-acc"),
    path('delete-account/(?P<person_id>[0-9]+)', views.delete_account, name="delete-acc"),
    path('course/(?P<person_id>[0-9]+)/(?P<course_id>[0-9]+)', views.course_page, name="course"),
    path('mycourses/(?P<person_id>[0-9]+)', views.mycourses, name="mycourses"),
    path('buy-course/(?P<person_id>[0-9]+)/(?P<course_id>[0-9]+)', views.buy_course, name="buycourse"),
    path('reloadtable/', views.reload_table),
    path('addcourse/(?P<person_id>[0-9]+)', views.add_course, name="addcourse"),
    path('check-addcourse/(?P<person_id>[0-9]+)', views.check_add_course, name="check-addcourse"),
    path('profile/(?P<person_id>[0-9]+)', views.profile, name="profile"),
    path('add-comment/(?P<person_id>[0-9]+)/(?P<course_id>[0-9]+)', views.add_comment, name="add-comment"),
    path('processdata/', views.process_data),
    path('report/(?P<person_id>[0-9]+)/(?P<course_id>[0-9]+)', views.submit_report, name="report"),
    path('add_favorite/(?P<person_id>[0-9]+)/(?P<course_id>[0-9]+)', views.add_favorite, name="favorite"),
    path('myfavorites/(?P<person_id>[0-9]+)', views.favorites, name="myfavorites"),
    path('change-pw/(?P<person_id>[0-9]+)', views.change_pw, name="change-pw"),
]