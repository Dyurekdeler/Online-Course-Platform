from django.shortcuts import render
import controller.controller as CONT
import query.macros as MACRO
from Model.models import Student
from view.forms import NameForm,signUpForm, idForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_login(request):

    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():

            username = form.data['username']
            password = form.data['password']
            get_credentials = CONT.get_from_db(MACRO.get_person_by_email(username))
            if get_credentials[0] == 'SUCCESS' and  len(get_credentials[1]) > 0 and get_credentials[1][0][4] == password:

                return profile(request, username)
            return render(request, "index.html", {'error':True})

    return render(request, 'index.html')

def index(request):
    return render(request, "index.html")

def sign_up(request):
    return render(request, "signup.html")

def profile(request,username):
    person_student = CONT.get_from_db(MACRO.get_person_student(username))
    if person_student[0] == 'SUCCESS' and person_student[1] is not None:
        return render(request, "profile.html", {'personid': person_student[1][0][0], 'firstname': person_student[1][0][1], 'lastname': person_student[1][0][2],'email': person_student[1][0][3],
                                                'password': person_student[1][0][4],'bday': person_student[1][0][5], 'address': person_student[1][0][6], 'phone': person_student[1][0][7],
                                                'university': person_student[1][0][11]})


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
                return render(request, "signup.html")
            else:
                student = Student(firstname, lastname, email, address, password1, bday, phone, None, university)
                created_person = CONT.get_from_db(MACRO.add_person(student.firstname,student.lastname,student.email,student.address,student.phone,student.bday,student.password))

                if created_person[0] == 'SUCCESS' and created_person[1][0][0] is not None:

                    if CONT.insert_db(MACRO.add_student_with_uni(created_person[1][0][0], student.universityId)) == 'SUCCESS':
                        return render(request, "index.html")
            return render(request,"signup.html") # db error

    return render(request, 'index.html')


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
            return render(request,"index.html")

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

                return render(request, "index.html")

    return render(request, 'profile.html')