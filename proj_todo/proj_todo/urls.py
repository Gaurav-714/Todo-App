from django.contrib import admin
from django.urls import path
from todo_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', signup_page, name = 'signup'),
    path('signin/', signin, name = 'signin'),
    path('signin/', signout, name = 'signout'),
    path('todo/', todo, name = 'todo'),
    path('update/<int:srno>', update, name = 'update'),
    path('delete/<int:srno>', delete, name = 'delete'),
]
