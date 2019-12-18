from django.contrib import messages
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

import controller.controller as CONT
import query.macros as MACRO
from Model.models import Student
from view.forms import loginForm,signUpForm, idForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, "home.html")

def sign_up(request):
    return render(request, "signup.html")

def login(request):
    return  render(request, "login.html")

def help(request):
    return render(request, "help.html")

def mycourses(request,person_id):
    return render(request, "mycourses.html", {'personid':person_id})

def profile(request,username):
    person_student = CONT.get_from_db(MACRO.get_person_student(username))
    if person_student[0] == 'SUCCESS' and person_student[1] is not None:
        return render(request, "profile.html", {'personid': person_student[1][0][0], 'firstname': person_student[1][0][1], 'lastname': person_student[1][0][2],'email': person_student[1][0][3],
                                                'password': person_student[1][0][4],'bday': person_student[1][0][5], 'address': person_student[1][0][6], 'phone': person_student[1][0][7],
                                                'university': person_student[1][0][11]})
@csrf_exempt
def check_login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)

        if form.is_valid():
            username = form.data['username']
            password = form.data['password']
            try:
                get_credentials = CONT.get_from_db(MACRO.user_login(username, password))
            except:
                return redirect("../home") #db error
            if len(get_credentials[1]) > 0 and get_credentials[1][0][4] == password:
                return profile(request, username) #succesful login

    messages.add_message(request, messages.INFO, "Invalid username or password!")
    return redirect('../login') #credentials does not match



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

            if password2 != password1:
                messages.add_message(request, messages.INFO, "Provided passwords does not match!")
                return redirect("../signup") #passwords do not match
            else:
                student = Student(firstname, lastname, email, address, password1, bday, phone, None, university)
                try:
                    CONT.insert_db(MACRO.add_person_student(student.firstname,student.lastname,student.email,student.address,student.phone,student.bday,student.password, student.universityId))
                    return redirect("../login/")
                except:
                    return redirect("../signup") # db error
    return redirect("../home/") # form is not valid error

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

def course(request):
    return render(request, "coursepage.html")

@csrf_exempt
def get_data(request):
    studentid = (request.POST.get('studentid' , False)) #get student id from frontend
    if studentid is not None:
        studentid = studentid.replace('"', '')
    try:
        ordered_courses = CONT.get_from_db(MACRO.get_ordered_courses(studentid)) #retrieve query set from db
    except Exception as ex:
        return JsonResponse({'status': '400', 'response': str(ex)}) #db error > warn front end
    #return HttpResponse(json.dumps(ordered_courses,cls=DjangoJSONEncoder),content_type="application/json") #db success, return the query set to front end
    return JsonResponse({'response':'200', 'data':ordered_courses[1]})