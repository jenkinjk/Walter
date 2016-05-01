from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import SugarTable

# Create your views here.
def index(request):
    template = loader.get_template('walter/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def history(request):
    user = 'jonathan_sux'
    user_info = SugarTable.objects.filter(username=user).order_by('-timestamp')
    context = {
        'user_info': user_info
    }

    return render(request, 'walter/history.html', context)

def insert(request):
    context = {}
    if request.method == 'POST':
        # do stuff
        context = {
            'added_message': "I added you to the database (promise)"
        }


    return render(request, 'walter/insert.html', context)
