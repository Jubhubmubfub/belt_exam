from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, 'belt/index.html')

def register(request):
    result = User.objects.validateReg(request)
    if result[0]==False:
        print_messages(request, result[1])
        return redirect('/')
    return log_user_in(request,result[1])

def success(request):
    if 'user' not in request.session:
        return redirect('/')
    return render(request, 'belt/success.html')

def login(request):
    result = User.objects.validateLogin(request)
    if result[0]==False:
        print_messages(request, result[1])
        return redirect('/')
    return log_user_in(request,result[1])

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.INFO, message)

def log_user_in(request,user):
    request.session['user'] = {
            'id':user.id,
            'first_name':user.first_name,
            'alias':user.alias,
            'email':user.email,
    }
    messages.add_message(request, messages.INFO, "successfully logged in! VALID EMAIL {}".format(request.POST['email']))
    return redirect('/success')

def logout(request):
    request.session.pop('user')
    return redirect('/')
