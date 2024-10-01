from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup_page, name = 'signup'),
    path('', signin, name = 'signin'),
    path('signout/', signout, name = 'signout'),
    path('todo/', todo, name = 'todo'),
    path('update/<int:srno>', update, name = 'update'),
    path('delete/<int:srno>', delete, name = 'delete'),
]
