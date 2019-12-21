
from django import forms

class loginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.PasswordInput()

class signUpForm(forms.Form):

    firstname = forms.CharField(label="fname",min_length=1,max_length=100)
    lastname = forms.CharField(label="lname",min_length=1,max_length=100)
    email = forms.CharField(label="email",min_length=1,max_length=100)
    address = forms.CharField(label="address",min_length=1,max_length=100)
    pw1 = forms.PasswordInput()
    pw2 = forms.PasswordInput()
    bday = forms.CharField(label="bday",min_length=1,max_length=100)
    phone = forms.CharField(label="phone",min_length=1,max_length=100)
    university = forms.CharField(label = "university",min_length=1, max_length=100)
    #personid = forms.CharField(label="personid",min_length=1,max_length=100)
    person_type = forms.CharField(label = "persontype",min_length=1, max_length=100)

class idForm(forms.Form):
    personid = forms.CharField(label="personid",min_length=1,max_length=100)

class courseForm(forms.Form):

    title = forms.CharField(label="title",min_length=1,max_length=100)
    description = forms.CharField(label="desc",min_length=1,max_length=100)
    price = forms.CharField(label="price",min_length=1,max_length=100)
    video_link = forms.CharField(label="videolink",min_length=1,max_length=1000000)
    category = forms.CharField(label="category",min_length=1,max_length=100)
    lecturer_id = forms.CharField(label="lecturerid",min_length=1,max_length=100)
    thumbnail = forms.CharField(label="thumbnail",min_length=1,max_length=10000000)

class commentForm(forms.Form):
    title = forms.CharField(label="title", min_length=1, max_length=100)
    description = forms.CharField(label="desc", min_length=1, max_length=250)



