from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import re, smtplib, auth

from .models import *

@login_required
def index(request):

    if request.method == 'POST':
        logout(request)
        return redirect('/walter/login')

    template = loader.get_template('walter/index.html')
    context = {'user': request.user}
    return HttpResponse(template.render(context, request))

@login_required
def history(request):
    user = request.user
    user_info = SugarTable.objects.filter(username=user).order_by('-timestamp')
    context = {
        'user_info': user_info
    }

    return render(request, 'walter/history.html', context)

@login_required
def configure(request):
    user = request.user
    context = {
        'user': user
    }

    if request.method == 'POST':
        post_data = request.POST

        number = validate_phone_number(post_data['phone'])
        carrier = post_data['carrier']

        phone_number = PhoneNumber(username=user, number=number, carrier=carrier)
        phone_number.save()

        context['added_message'] = 'Added your phone number ' + post_data['phone'] + '. Test it below'

    return render(request, 'walter/configuration.html', context)

def validate_phone_number(number):
    return number

@login_required
def insert(request):
    context = {}
    if request.method == 'POST':
        # Add reading to database
        post_data = request.POST
        user = SugarTable(username=request.user, blood_sugar=post_data['blood_sugar'], timestamp=timezone.now())
        user.save()

        context = {
            'added_message': "Your most recent reading of " + post_data['blood_sugar'] + " has been saved."
        }


    return render(request, 'walter/insert.html', context)


def register(request):
    context = {}
    if request.method == 'POST':
        post_data = request.POST
        added_message = ""
        if post_data['username'] == "":
            added_message = added_message+"Please input a username. "
        if post_data['email'] == "":
            added_message = added_message+"Please input an email. Make sure it is a valid one. "
        elif not (re.match(r"[^@]+@[^@]+\.[^@]+", post_data['email'])):
            added_message = added_message+"You have entered an invalid email. "
        if post_data['password'] == "":
            added_message = added_message+"Please input a password. "
        if post_data['password'] == "":
            added_message = added_message+"Please reinput a password for verification. "
        if post_data['password'] != post_data['password2']:
            added_message = added_message+'Password fields must match '
        if(User.objects.filter(username = post_data['username']).exists()):
            added_message = added_message + "This username is already in use: "+post_data['username']+"\n"
        if(User.objects.filter(email = post_data['email']).exists()):
           added_message=added_message + "This email is already in use: "+post_data['email']+"\n"
        if(added_message == ""):
            user = User.objects.create_user(post_data['username'], post_data['email'], post_data['password'])
            user.save()
            user = authenticate(username=post_data['username'], password=post_data['password'])
            login(request, user)

            added_message = 'You have been registered!'
            return redirect('/walter')
        context={ "added_message":added_message}
    return render(request, 'walter/register.html', context)

def signin(request):
    context = {}
    if request.method == 'POST':
        post_data = request.POST

        user = authenticate(username=post_data['username'], password=post_data['password'])

        if user is None:
            added_message = 'Invalid username or password'
        else:
            login(request, user)
            return redirect('/walter')

        context = {
            'added_message': added_message
        }

    return render(request, 'walter/login.html', context)

@login_required
def testText(request):
    context = {
        'added_message': "A text was sent to "
    }

    if request.method == 'POST':
        post_data = request.POST

        test_number = post_data['test']
        number = PhoneNumber.objects.get(username=request.user, number=test_number)

        send_mail(number.number, number.carrier)
        context = {
            'added_message': 'A text was sent to ' + test_number
        }

    return render(request, 'walter/configuration.html', context)

def send_mail(number, carrier):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login( auth.EMAIL_ADDRESS, auth.EMAIL_PASSWORD )

    server.sendmail('From: Walter Project', number + '@' + carrier, 'This is a test text message!')
