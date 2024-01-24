from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

def signup_page(request):
    if request.method == 'POST':

        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user = User.objects.filter(username = username)
            if user.exists():
                messages.warning(request, "Username Is Already Taken.")
                return redirect('/')
            
            user = User.objects.create(username = username, email = email)
            user.set_password(password)
            user.save()

            messages.success(request, "Account Created.")
            return redirect('/signin/')

        except:
            messages.warning(request, "Something Went Wrong...")
            return redirect('/')
        
    return render(request, 'signup.html')


@login_required(login_url = '/signin/')
def signin(request):
    if request.method == 'POST':

        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.filter(username = username)
            if not user.exists():
                messages.warning(request, "Username Not Found.")
                return redirect('/signin/')
            
            user = authenticate(username = username, password = password)
            if user:
                login(request, user)
                return redirect('/todo/')
            else:
                messages.warning(request, "Incorrect Password")
                return redirect('/signin/')
        
        except:
            messages.warning(request, "Something Went Wrong...")
            return redirect('/signin/')

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('/signin/')


@login_required(login_url = '/signin/')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        obj = Todo(title = title, user = request.user)
        obj.save()
        todos = Todo.objects.filter(user = request.user).order_by('date')
        return redirect('/todo/', {'todos' : todos})
    
    todos = Todo.objects.filter(user = request.user).order_by('date')
    return render(request, 'todo.html', {'todos' : todos})


@login_required(login_url = '/signin/')
def update(request, srno):
    if request.method == 'POST':

        title = request.POST.get('title')
        todos = Todo.objects.filter(user = request.user, srno = srno)
        todos.title = title
        todos.save()
        return redirect('/todo/')
    
    todos = Todo.objects.filter(user = request.user).order_by('date')
    return render(request, 'update.html', {'todos' : todos})


@login_required(login_url = '/signin/')
def delete(request, srno):
    todos = Todo.objects.get(user = request.user, srno = srno)
    todos.delete()
    return redirect('/todo/')
