"""
URL configuration for studentstudyportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from studentdashboard import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.home),
    path('notes/', views.notes, name='notes'),
    path('delete_note/<pk>',views.delete_note,name="delete-note"),
  
    path('notesd/<pk>',views.notesd,name="notesd"),
    path('homework/', views.homework, name='homework'),
    path('updatehomework/<pk>',views.updatehomework,name = 'updatehomework'),
    path('delete_homework/<pk>',views.delete_homework,name = 'delete-homework'),
    path('youtube',views.youtube,name = 'youtube'),
    path('todo',views.todo,name = 'todo'),
    path('updatetodo/<pk>',views.updatetodo,name = 'updatetodo'),
    path('delete_todo/<pk>',views.delete_todo,name = 'delete-todo'),
    path('books',views.books,name = 'books'),
    path('dictionary',views.dictionary,name = 'dictionary'),
    path('wiki',views.wiki,name = 'wiki'),
    path('conversion',views.conversion,name = 'conversion'),
    path('register',views.register,name = 'register'),
    path('userlogin',views.userlogin,name = 'userlogin'),
    path('userlogout',views.userlogout,name= 'userlogout'),
    path('forgot/<pk>', views.forgot, name='forgot'),



    

        

]





