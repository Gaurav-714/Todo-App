from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

def signup_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = User.objects.filter(username = username).first()
            if user:
                messages.warning(request, "*** Username Is Already Taken ***")
                return redirect('/')
            
            user = User.objects.create(username = username)
            user.set_password(password)
            user.save()

            messages.success(request, "*** Account Created. Kindly Sign-In. ***")
            return redirect('signin')

        except:
            messages.warning(request, "*** Something Went Wrong ***")
            return redirect('/')
        
    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.filter(username = username).first()
            if not user:
                messages.warning(request, "*** User Not Found. Create Account. ***")
                return redirect('signup')
            
            user = authenticate(username = username, password = password)
            if user:
                login(request, user)
                return redirect('todo')
            else:
                messages.warning(request, "*** Incorrect Password. Try Again. ***")
                return redirect('/')
        
        except:
            messages.warning(request, "*** Something Went Wrong ***")
            return redirect('/')

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url = '/')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        obj = Todo(title = title, user = request.user)
        obj.save()
        
        todos = Todo.objects.filter(user = request.user).order_by('date')
        return redirect('/todo/', {'todos' : todos})
    
    todos = Todo.objects.filter(user = request.user).order_by('date')
    return render(request, 'todo.html', {'todos' : todos})


@login_required(login_url = '/')
def update(request, srno):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            #status = request.POST.get('status')
            todo = Todo.objects.get(user = request.user, srno = srno)
            todo.title = title
            #todo.status = status
            todo.save()
            return redirect('todo', {'todo' : todo})
        except Exception as ex:
            print(ex)
            return redirect('todo')
    
    todo = Todo.objects.filter(srno = srno).first()
    return render(request, 'update.html', {'todo' : todo})


@login_required(login_url = '/')
def delete(request, srno):
    todos = Todo.objects.get(user = request.user, srno = srno)
    todos.delete()
    return redirect('todo')
