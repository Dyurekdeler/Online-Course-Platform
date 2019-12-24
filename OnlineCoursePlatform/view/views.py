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
from view.forms import loginForm, signUpForm, courseForm, commentForm, reportForm, passwordForm, \
    profileChangeForm
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
    sent_comments = None
    sent_is_bought = False
    course = CONT.get_from_db(MACRO.get_course(course_id))  # retrieve query set from db
    if (course[0] == 'SUCCESS' and len(course[1]) > 0):
        cmnt_counts = CONT.get_from_db(MACRO.get_comment_counts(course_id))
        if cmnt_counts[0] == 'SUCCESS' and len(cmnt_counts[1][0]) > 0:
            if cmnt_counts[1][0][1]>0:
                comments = CONT.get_from_db(MACRO.get_course_comments(course_id))
                if comments[0] == 'SUCCESS' and len(comments[1][0]) > 0:
                    sent_comments = comments[1]
                else:
                    #exit comment count is bigger than 0 but comment does not exits
                    return redirect(reverse('home', kwargs={'person_id': person_id}))  # when there is no course
            else:
                #comment 0 dan azdır commentsiz gönder
                sent_comments = None
        else:
            #exit comment count could not reached
            return redirect(reverse('home', kwargs={'person_id': person_id}))  # when there is no course
        if person_id != '0':
            user = CONT.get_from_db(MACRO.get_user_type(person_id))
            if user[0] == 'SUCCESS' and len(user[1][0]) > 0:
                order = CONT.get_from_db(MACRO.get_bought_course(course_id, person_id))
                if order[0] == 'SUCCESS' and len(order[1][0]) > 0:
                    sent_is_bought = True
                else:
                    sent_is_bought = False
                if sent_comments is not None:
                    return render(request, "coursepage.html",
                                  {'course': course[1][0], 'comments': sent_comments[1], 'personid': person_id,
                                   'persontype': user[1][0][1], 'bought': sent_is_bought})
                else:
                    return render(request, "coursepage.html",
                                  {'course': course[1][0], 'personid': person_id,
                                   'persontype': user[1][0][1], 'bought': sent_is_bought})
            else:
                #exit useer not found
                return redirect(reverse('home', kwargs={'person_id': person_id}))  # when there is no course
        else:
            if sent_comments is not None:
                return render(request, "coursepage.html",
                              {'course': course[1][0], 'comments': sent_comments[1], 'personid': person_id,
                               'persontype': 'guest'})
            else:
                return render(request, "coursepage.html",
                              {'course': course[1][0],  'personid': person_id,
                               'persontype': 'guest'})


    else:
        #exit course not found
        return redirect(reverse('home', kwargs={'person_id': person_id}))  # when there is no course

    return redirect(reverse('home', kwargs={'person_id': person_id})) #when there is no course

def profile(request, person_id):
    user = CONT.get_from_db(MACRO.get_user_by_id(person_id))
    try:
        unis = CONT.get_from_db(MACRO.GET_ALL_UNIS)  # retrieve query set from db
        if user[0] == 'SUCCESS' and len(user[1]) > 0:
            uni = CONT.get_from_db(MACRO.get_user_uni(user[1][0][0], user[1][0][8]))
            if uni[0] == 'SUCCESS' and len(uni[1]) > 0:
                user = user[1][0]
                return render(request, "profile.html",
                              {'personid': user[0], 'firstname': user[1], 'lastname': user[2], 'email': user[3],
                               'password': user[4], 'bday': user[5], 'address': user[6], 'phone': user[7],
                               'persontype': user[8], 'university': uni[1][0][0], 'universities':unis[1]})
    except Exception:
        return redirect(reverse('home', kwargs={'person_id': person_id}))

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
                try:
                    if person_type == 'STU':
                        student = Student(firstname, lastname, email, address, password1, bday, phone, university)
                        CONT.call_proc(MACRO.add_person(student.firstname,student.lastname,student.email,student.password,student.bday,student.address,student.phone, student.universityId,person_type))
                    elif person_type == 'LEC':
                        lecturer = Lecturer(firstname, lastname, email, address, password1, bday, phone, university)
                        CONT.call_proc(MACRO.add_person(lecturer.firstname, lecturer.lastname, lecturer.email, lecturer.password,  lecturer.bday,lecturer.address,lecturer.phone, lecturer.universityId,person_type))

                    return redirect(reverse('login', kwargs={'person_id': '0'}))  #navigate user to login with newly created account
                except:
                    return redirect(reverse('signup', kwargs={'person_id': '0'}))  #db error
    return redirect(reverse('home', kwargs={'person_id': '0'}))  #form is not valid

def update_account(request,person_id):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = profileChangeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            firstname = form.data['firstname']
            lastname = form.data['lastname']
            email = form.data['email']
            phone = form.data['phone']
            address = form.data['address']
            bday = form.data['bday']
            university = form.data['university']


            #BURAYA UNI YI DE UPDATE EDECEK TRIGGER VEYA PROCEDURE YAZZZZ SUANKI HALI BOZUK



            try:
                CONT.update_db(MACRO.update_person(person_id, firstname, lastname, email, address, phone, bday, university))
                return profile(request, person_id)
            except:
                return render(request,"home.html")
    return render(request, 'profile.html')

def delete_account(request,person_id):
    #BURAYA DELETE PROCEDUR YAZMALIYIZ
    pass

def change_pw(request, person_id):
    if request.method == 'POST':

        form = passwordForm(request.POST)

        if form.is_valid():

            new_pw = form.data['pw1']
        try:
            CONT.update_db(MACRO.update_password(person_id, new_pw))
            return render(request, 'profile.html')
        except:
            return render(request, "home.html")
    return render(request, "home.html")

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
    elif table_id == 'university':
        table_data = CONT.get_from_db(MACRO.GET_ALL_UNIS)
    elif table_id == 'student':
        table_data = CONT.get_from_db(MACRO.GET_ALL_STUDENTS)
    elif table_id == 'lecturer':
        table_data = CONT.get_from_db(MACRO.GET_ALL_LECTURERS)
    elif table_id == 'course':
        table_data = CONT.get_from_db(MACRO.GET_ALL_COURSES)
    elif table_id == 'comment':
        table_data = CONT.get_from_db(MACRO.GET_ALL_COMMENTS)
    elif table_id == 'report':
        table_data = CONT.get_from_db(MACRO.GET_ALL_REPORTS)
    elif table_id == 'order':
        table_data = CONT.get_from_db(MACRO.GET_ALL_ORDERS)
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


@csrf_exempt
def process_data(request):
    intent = (request.POST.get('intent', False)).strip('/"')
    table_id = (request.POST.get('table_id', False)).strip('/"')
    data_id = (request.POST.get('data_id', False)).strip('/"')
    newvalue1 = (request.POST.get('newvalue1', False))
    newvalue2 = (request.POST.get('newvalue2', False))
    newvalue3 = (request.POST.get('newvalue3', False))
    newvalue4 = (request.POST.get('newvalue4', False))
    newvalue5 = (request.POST.get('newvalue5', False))
    newvalue6 = (request.POST.get('newvalue6', False))
    newvalue7 = (request.POST.get('newvalue7', False))
    newvalue8 = (request.POST.get('newvalue8', False))
    newvalue9 = (request.POST.get('newvalue9', False))


    if newvalue1 != None:
        newvalue1 = newvalue1.strip('/"')
    if newvalue2 != None:
        newvalue2 = newvalue2.strip('/"')
    if newvalue3 != None:
        newvalue3 = newvalue3.strip('/"')
    if newvalue4 != None:
        newvalue4 = newvalue4.strip('/"')
    if newvalue5 != None:
        newvalue5 = newvalue5.strip('/"')
    if newvalue6 != None:
        newvalue6 = newvalue6.strip('/"')
    if newvalue7 != None:
        newvalue7 = newvalue7.strip('/"')
    if newvalue8 != None:
        newvalue8 = newvalue8.strip('/"')
    if newvalue9 != None:
        newvalue9 = newvalue8.strip('/"')

    if table_id == 'person':
        query = MACRO.add_person(newvalue1, newvalue2, newvalue3,newvalue4, newvalue5, newvalue6, newvalue7, newvalue8,  newvalue9)
        if intent == 'edit':
            query = MACRO.update_person(data_id, newvalue1, newvalue2, newvalue3)
    elif table_id == 'university':
        query = MACRO.add_clicksrc(newvalue1, newvalue2)
        if intent == 'edit':
            query = MACRO.update_clicksrc(data_id, newvalue1, newvalue2)
    elif table_id == 'course':
        query = MACRO.add_language(newvalue1, newvalue2, newvalue3)
        if intent == 'edit':
            query = MACRO.update_language(data_id, newvalue1, newvalue2, newvalue3)
    elif table_id == 'comment':
        query = MACRO.add_serviceproperty(newvalue1, newvalue2)
        if intent == 'edit':
            query = MACRO.update_serviceproperty(data_id, newvalue1, newvalue2)
    elif table_id == 'report':
        query = MACRO.add_ad(newvalue1, newvalue2)
        if intent == 'edit':
            query = MACRO.update_ad(data_id, newvalue1, newvalue2)
    elif table_id == 'order':
        query = MACRO.add_adConfig(newvalue1, newvalue2, newvalue3, newvalue4)
        if intent == 'edit':
            query = MACRO.update_adConfig(data_id, newvalue1, newvalue2, newvalue3, newvalue4)
    else:
        query = None
    if intent == 'add':
        if table_id == 'ad':
            try:
                auto_created_id = CONT.get_from_db(query, request.session['database'])[0][0]
            except Exception as ex:
                return JsonResponse({'status': '400', 'response': str(ex)})
            return JsonResponse(
                {'status': '200', 'response': 'Added the new record :' + str(data_id) + ' successfully!',
                 'auto_created_id': auto_created_id})
        else:
            try:
                CONT.insert_db(query, request.session['database'])
            except Exception as ex:
                return JsonResponse({'status': '400', 'response': str(ex)})
        return JsonResponse({'status': '200', 'response': 'Added the new record :' + str(data_id) + ' successfully!'})

    elif intent == 'edit':
        try:
            CONT.update_db(query, request.session['database'])
        except Exception as ex:
            return JsonResponse({'status': '400', 'response': str(ex)})
    return JsonResponse({'status': '200', 'response': 'Updated the data :' + str(data_id) + '!'})

@csrf_exempt
def submit_report(request, person_id, course_id):
    if request.method == 'POST':
        form = reportForm(request.POST)

        if form.is_valid():
            report_description = form.data['report_description']
            today = date.today()
            report_date = today.strftime("%d/%m/%Y")
            try:
                CONT.insert_db(MACRO.add_report_to_course(person_id,report_description,course_id,report_date))
                return redirect(reverse('course', kwargs={'person_id': person_id, 'course_id':course_id}))
            except:
                return redirect(reverse('home', kwargs={'person_id': person_id}))
    return redirect(reverse('home', kwargs={'person_id': '0'}))

@csrf_exempt
def add_favorite(request, person_id, course_id):
    try:
        CONT.insert_db(MACRO.add_favorite(person_id, course_id))
        return redirect(reverse('course', kwargs={'person_id': person_id, 'course_id':course_id}))
    except:
        return redirect(reverse('home', kwargs={'person_id': person_id}))
    return redirect(reverse('home', kwargs={'person_id': '0'}))

def favorites(request, person_id):
    favs = CONT.get_from_db(MACRO.get_users_favorites(person_id))
    if favs[0] == 'SUCCESS' and len(favs[1][0])>0:
        return render(request, "favoritecourses.html", {'personid':person_id, 'courses':favs[1]})
    return redirect(reverse('home', kwargs={'person_id': person_id}))