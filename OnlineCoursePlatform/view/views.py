from django.contrib import messages
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
import json
from datetime import date
import controller.controller as CONT
import query.macros as MACRO
from Model.Student import Student
from Model.Lecturer import Lecturer
from view.forms import loginForm,signUpForm, idForm, courseForm, commentForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

def home(request):
    return redirect(reverse('home', kwargs={'person_id': '0'}))

def home_user(request,person_id):
    courses = CONT.get_from_db(MACRO.GET_ALL_COURSES)  # retrieve query set from db
    if courses[0] == 'SUCCESS' and len(courses[1]) > 0:
        if person_id == '0':
            return render(request, "home.html", {'courses':courses[1], 'personid':person_id, 'persontype':'notype'})
        else:
            person_name_type = CONT.get_from_db(MACRO.get_user_type(person_id))
            if person_name_type[0] == 'SUCCESS' and len(person_name_type[1]) > 0:
                if person_name_type[1][0][1] == 'STU':
                    return render(request, "home.html", {'courses':courses[1], 'personid':person_id, 'personname':person_name_type[1][0][0], 'persontype':person_name_type[1][0][1]})
                else:
                    return render(request, "home.html", {'personid':person_id, 'personname':person_name_type[1][0][0], 'persontype':person_name_type[1][0][1]})
    return redirect(reverse('home', kwargs={'person_id': person_id})) # error for courses

def sign_up(request,person_id):
    try:
        unis = CONT.get_from_db(MACRO.GET_ALL_UNIS)  # retrieve query set from db
    except Exception:
        return redirect(reverse('home', kwargs={'person_id': person_id}))
    return render(request, "signup.html", {'universities':unis[1], 'personid':person_id})

def login(request,person_id):
    return render(request, "login.html", {'personid':person_id})

def mycourses(request,person_id):
    person_type = CONT.get_from_db(MACRO.get_user_type(person_id))
    print(person_type)
    if person_type[0] == 'SUCCESS' and len(person_type[1])>0:
        if(person_type[1][0][1] == 'STU'):
            ordered_courses = CONT.get_from_db(MACRO.get_ordered_courses(person_id))  # retrieve query set from db
            if ordered_courses[0] == 'SUCCESS' and len(ordered_courses[1])>0:
                return render(request, "mycourses.html", {'personid':person_id, 'persontype':person_type[1][0][1], 'courses':ordered_courses[1]})
        else:
            lecturer_courses = CONT.get_from_db(MACRO.get_course_of_lecturer(person_id))
            if lecturer_courses[0] == 'SUCCESS' and len(lecturer_courses[1]) > 0:
                return render(request, "mycourses.html", {'personid':person_id,  'persontype':person_type[1][0][1], 'courses':lecturer_courses[1]})
    return redirect(reverse('home', kwargs={'person_id': person_id}))

def admin(request):
    return render(request, "admin.html")

def add_course(request, person_id):
    return render(request, "addcourse.html", {'personid':person_id})

@csrf_exempt
def course_page(request,person_id,course_id):
    course = CONT.get_from_db(MACRO.get_course(course_id))  # retrieve query set from db
    if course[0] == 'SUCCESS' and len(course[1])>0:
        comments = CONT.get_from_db(MACRO.get_course_comments(course_id))
        print(comments)
        if comments[0] == 'SUCCESS' and len(comments[1])>0:
            if person_id == '0':
                return render(request, "coursepage.html", {'course':course[1][0], 'comments':comments[1], 'personid':person_id, 'bought':False})
            is_bought = CONT.get_from_db(MACRO.get_bought_course(course_id, person_id))
            if is_bought[0] == 'SUCCESS' and len(is_bought[1])>0:
                return render(request, "coursepage.html", {'course':course[1][0], 'comments':comments[1],'personid':person_id, 'bought':True})
            return render(request, "coursepage.html", {'course': course[1][0], 'comments':comments[1], 'personid': person_id, 'bought': False})
    return redirect(reverse('home', kwargs={'person_id': person_id})) #when there is no course

def profile(request, person_id):
    user = CONT.get_from_db(MACRO.get_user_by_id(person_id))
    if user[0] == 'SUCCESS' and len(user[1]) > 0:
        uni = CONT.get_from_db(MACRO.get_user_uni(user[1][0][0], user[1][0][8]))
        if uni[0] == 'SUCCESS' and len(uni[1]) > 0:
            user = user[1][0]
            return render(request, "profile.html", {'personid': user[0], 'firstname': user[1], 'lastname': user[2],'email': user[3],
                                                'password': user[4],'bday': user[5], 'address': user[6], 'phone': user[7],
                                               'persontype':user[8], 'university':uni[1][0][0]})
    return redirect(reverse('home', kwargs={'person_id':'0'}))  # when there are db error

@csrf_exempt
def check_login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)

        if form.is_valid():
            username = form.data['username']
            password = form.data['password']
            user = CONT.get_from_db(MACRO.get_user(username, password))
            if user[0] == 'SUCCESS' and len(user[1])>0:
                return redirect(reverse('profile', kwargs={'person_id': user[1][0][0]})) # succesful login
            messages.add_message(request, messages.INFO, "Invalid username or password!")
            return redirect(reverse('login', kwargs={'person_id': '0'}))  # credentials does not match
        return redirect(reverse('home', kwargs={'person_id': '0'}))

@csrf_exempt
def check_signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = signUpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            firstname = form.data['firstname']
            lastname = form.data['lastname']
            email = form.data['email']
            address = form.data['address']
            password1 = form.data['pw1']
            password2 = form.data['pw2']
            bday = form.data['bday']
            phone = form.data['phone']
            university = form.data['university']
            person_type = form.data['person_type']
            
            if password2 != password1:
                messages.add_message(request, messages.INFO, "Provided passwords does not match!")
                return redirect(reverse('signup', kwargs={'person_id': '0'})) #passwords do not match
            else:
                if person_type == 'STU':
                    student = Student(firstname, lastname, email, address, password1, bday, phone, university)
                    try:
                        CONT.insert_db(MACRO.add_person_student(student.firstname,student.lastname,student.email,student.address,student.phone,student.bday,student.password, student.universityId))
                        return redirect(reverse('login', kwargs={'person_id': '0'}))  #navigate user to login with newly created account
                    except:
                        return redirect(reverse('signup', kwargs={'person_id': '0'}))  #db error
                else:
                    lecturer = Lecturer(firstname, lastname, email, address, password1, bday, phone, university)
                    try:
                        CONT.insert_db(MACRO.add_person_lecturer(lecturer.firstname, lecturer.lastname, lecturer.email,
                                                                lecturer.address, lecturer.phone, lecturer.bday,
                                                                lecturer.password, lecturer.universityId))
                        return redirect(reverse('login', kwargs={'person_id': '0'}))  #navigate user to login with newly created account
                    except:
                        return redirect(reverse('signup', kwargs={'person_id': '0'}))  #db error
    return redirect(reverse('home', kwargs={'person_id': '0'}))  #form is not valid

def update_account(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = signUpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            firstname = form.data['firstname']
            lastname = form.data['lastname']
            email = form.data['email']
            address = form.data['address']
            password1 = form.data['pw1']
            password2 = form.data['pw2']
            bday = form.data['bday']
            phone = form.data['phone']
            university = form.data['university']
            personid = form.data['personid']

            #check old pw is correct
            if CONT.update_db(MACRO.update_person(personid, firstname, lastname, email, address, phone, bday, password2)) == 'SUCCESS':
                return profile(request, email)
            return render(request,"home.html")

    return render(request, 'profile.html')

def delete_account(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = idForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

            personid = form.data['personid']

            # check old pw is correct
            if CONT.update_db(MACRO.delete_student(personid))=='SUCCESS' and CONT.update_db(MACRO.delete_person(personid)) == 'SUCCESS':

                return render(request, "home.html")
    return render(request, 'profile.html')

def buy_course(request,person_id,course_id):
    today = date.today()
    order_date = today.strftime("%d/%m/%Y")
    try:
        CONT.insert_db(MACRO.buy_course(person_id, course_id, order_date))
        return redirect(reverse('course', kwargs={'person_id': person_id, 'course_id':course_id}))
    except Exception:
        return redirect(reverse('home', kwargs={'person_id': person_id}))

@csrf_exempt
def reload_table(request):
    table_id = (request.GET.get('table_id' , False)).strip('/"')
    if table_id == 'person':
        table_data = CONT.get_from_db(MACRO.GET_ALL_PEOPLE)
    else:
        table_data = None
    return HttpResponse(json.dumps(table_data[1],cls=DjangoJSONEncoder),content_type="application/json")

@csrf_exempt
def check_add_course(request,person_id):
    if request.method == 'POST':
        form = courseForm(request.POST)

        if form.is_valid():
            title = form.data['title']
            description = form.data['description']
            price = form.data['price']
            video_link = form.data['video_link']
            category = form.data['category']
            lecturer_id = form.data['lecturer_id']
            thumbnail = form.data['thumbnail']
            try:
                CONT.insert_db(MACRO.add_course(title, description, price, video_link, category, lecturer_id, thumbnail))
                return redirect(reverse('mycourses', kwargs={'person_id': person_id}))
            except:
                return redirect(reverse('home', kwargs={'person_id': person_id}))
    return redirect(reverse('home', kwargs={'person_id': person_id}))

@csrf_exempt
def add_comment(request,person_id, course_id):
    if request.method == 'POST':
        form = commentForm(request.POST)

        if form.is_valid():
            title = form.data['title']
            description = form.data['description']

            today = date.today()
            cmt_date = today.strftime("%d/%m/%Y")
            try:
                CONT.insert_db(MACRO.add_comment_to_course(person_id,description,title,course_id,cmt_date))
                return redirect(reverse('course', kwargs={'person_id': person_id, 'course_id':course_id}))
            except:
                return redirect(reverse('home', kwargs={'person_id': person_id}))
    return redirect(reverse('home', kwargs={'person_id': '0'}))