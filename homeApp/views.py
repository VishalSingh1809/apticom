from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from homeApp import forms
from homeApp.models import UserSignUp
from django.views.generic import ListView
from random import *
from django.contrib.auth import authenticate
from django.http import HttpResponse

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from twilio.rest import Client
ACCOUNT_SID='AC41482afa413cd54f00ab373c0cbbaca6'
AUTH_TOKEN='ff8b5d117fc669ac5b4e8e8020f81498'

# Create your views here.
def home(request):
    return render(request,'homeApp/home.html')


def aboutus(request):
    return render(request,'homeApp/aboutus.html')


def contactus(request):
    return render(request,'homeApp/contactus.html')


def services(request):
    return render(request,'homeApp/services.html')



def generate_otp():
    s=''
    i=0
    while(i<6):
            s=s+str(randint(0,9))
            i=i+1
    return int(s)


@login_required
def quant_exam(request):
    return render(request,'homeApp/exampage.html')


@login_required
def verbal_exam(request):
    return render(request,'homeApp/exampage.html')


@login_required
def logical_exam(request):
    return render(request,'homeApp/exampage.html')


@login_required
def profile_home(request):
    return render(request,'users/profile.html')


def sign_up(request):
    form=forms.SignUpForm()
    if(request.method=='POST'):
        form=forms.SignUpForm(request.POST)
        if(form.is_valid()):
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(user.password)
            user.save()
            current_site = get_current_site(request)
            username=form.cleaned_data['username']
            phonenumber=form.cleaned_data['phonenumber']
            mail_subject = 'Apticom Careers activation link. Please activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    return render(request,'registration/signup.html',{'form':form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserSignUp.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified= True
        otp=int(generate_otp())
        print(otp)
        user.phonenumber_otp=otp
        user.save()
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
                              body='Hello there! Your OTP is'+str(otp),
                              from_='+19794818210',
                              to='+91'+str(user.phonenumber)
                          )

        my_dict={
        'uid':uid,
        'number':user.phonenumber
        }
        return render(request,'registration/verifynumber.html',context=my_dict)
    else:
        return HttpResponse('Activation link is invalid!')




def verify_number(request):
    if(request.method=='POST'):
        uid=request.POST['uid']
        otp=request.POST['otp']
        user = UserSignUp.objects.get(pk=uid)
        genotp=user.phonenumber_otp
        print(genotp)
        print(otp)
        print(uid)
        if(str(genotp)==str(otp)):
            user.phonenumber_verified=True
            user.is_active=True
            user.save()
        else:
            print("wrogn otp************************************")
        return render(request,'homeApp/home.html')



def login(request):
    if(request.method=='POST'):
        username=request.POST['username']
        password=request.POST['password']
        user= UserSignUp.objects.get(username=request.POST['username'])
        print(user)
        if user is None:
            return render(request,'registration/login.html',{'msg':'Please check username and password'})
            return HttpResponse('<h1>Username and Password is invalid<h1>')
        else:
            firstname=user.first_name
            lastname=user.last_name
            SESSION_COOKIE_AGE = 60 * 60 * 24 * 30 # One month
            request.session['member_id']=user.id
            print(request.session['member_id'])
            request.session['name']=firstname+lastname
            name=request.session['name']
            my_dict={
                'name':name
            }
            return render(request,'homeApp/services.html',context=my_dict)
    else:
        return redirect('/accounts/login')
        return HttpResponse('<h1>Username and Password is invalid<h1>')
