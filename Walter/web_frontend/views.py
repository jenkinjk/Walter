from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import SugarTable

@login_required
def index(request):

    if request.method == 'POST':
        logout(request)
        return redirect('/walter/login')

    template = loader.get_template('walter/index.html')
    context = {}
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
def insert(request):
    context = {}
    if request.method == 'POST':
        # Add reading to database
        post_data = request.POST
        user = SugarTable(username=request.user, blood_sugar=post_data['blood_sugar'], timestamp=timezone.now())
        user.save()

        context = {
            'added_message': "I added you to the database"
        }


    return render(request, 'walter/insert.html', context)


def register(request):
    context = {}
    if request.method == 'POST':
        post_data = request.POST

        if post_data['password'] != post_data['password2']:
            added_message = 'Password fields must match'
        else:
            user = User.objects.create_user(post_data['username'], post_data['email'], post_data['password'])
            user.save()

            added_message = 'You have been registered!'
            return redirect('/walter/login')

        context = {
            'added_message': added_message
        }

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
