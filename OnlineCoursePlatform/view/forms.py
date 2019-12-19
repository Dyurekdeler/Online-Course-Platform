
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
