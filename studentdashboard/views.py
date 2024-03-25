from django.shortcuts import render,redirect,HttpResponse
from .forms import*
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')



@login_required(login_url="/userlogin")
def notes(request):
    if request.method == 'POST':
        form  = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user = request.user,title = request.POST['title'],description = request.POST['description'])
            notes.save()
        messages.success(request,f'Notes added from  {request.user.username}  sucessfully!')
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes,'form':form}
    return render(request, 'dashboard/notes.html',context)
  

@login_required(login_url="/userlogin")
def delete_note(request,pk):
    
    m=Notes.objects.filter(id = pk)
    m.delete()
    return redirect('/notes')





from django.shortcuts import render, get_object_or_404
from .models import Notes


def notesd(request, pk):
    # Retrieve the note from the database based on the provided 'pk' (primary key)
    note = get_object_or_404(Notes, id=pk)

    # Pass the note to the template context
    context = {'note': note}

    # Render the template with the provided context
    return render(request, 'notesd.html', context)




@login_required(login_url="/userlogin")
def homework(request):
    if request.method =='POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']   
                if finished == 'on':        #If the checkbox is checked ('on' in POST data), finished is set to True; 
                    finished = True
                else:
                    finished = False      # otherwise false
            except:
                finished = False
            homeworks = Homework(                            #a new Homework object is created with the# user, subject, title, description, due date, and whether it is finished or not. The object is then saved to the database.
                user = request.user,                           # user, subject, title, description, due date, 
                subject = request.POST['subject'],                        #and whether it is finished or not. The object is then saved to the database.
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()                               # save the homework in homeworks variable
            messages.success(request,f"Homework Added from{request.user.username}!!!")
    else:   
                
        form = HomeworkForm()
    homework = Homework.objects.filter(user = request.user)     # if the request is not post,a new instance of the HomeworkForm class is creted
    if len(homework)==0:                                         #This is typically used for rendering an empty form for the user to fill out.
        homework_done = True
    
    else:
        homework_done = False
        
    context = {'homeworks':homework,'homeworks_done':homework_done,'form':form}
    return render (request,'dashboard/homework.html',context)




@login_required(login_url="/userlogin")
def updatehomework(request,pk):
    homework = Homework.objects.get(id = pk)
    if homework.is_finished == True:
        homework.is_finished = False
    
    else:
        homework.is_finished = True
    homework.save()
    return redirect('/homework')




@login_required(login_url="/userlogin")
def delete_homework(request,pk):
    
    m=Homework.objects.filter(id = pk)
    m.delete()
    return redirect('/homework')


@login_required(login_url="/userlogin")
def youtube(request):
    if request.method == 'POST':
        form = Dashboardform(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit = 10)
        result_list = []
        for i in video.result()['result']:
            result_dict ={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render (request,'dashboard/youtube.html',context)
    else:
        form = Dashboardform()
    context = {'form':form}
    return render(request,"dashboard/youtube.html",context)




@login_required(login_url="/userlogin")
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(user = request.user, 
                         title = request.POST['title'],
                        is_finished = finished
                        )
            todos.save()
            messages.success(request,f"Todo Added from {request.user.username} sucessfully !!")
    else:  
        form = TodoForm()
    todo = Todo.objects.filter(user = request.user)
    if len(todo) == 0:
        todos_done = True
        
    else:
        todos_done = False
    context = {
        'form':form,
        'todos':todo,
        'todos_done':todos_done
    }
    return render(request,'dashboard/todo.html',context)




@login_required(login_url="/userlogin")
def updatetodo(request,pk):
    todo = Todo.objects.get(id = pk)
    if todo.is_finished == True:
        todo.is_finished = False
    
    else:
        todo.is_finished = True
    todo.save()
    return redirect('/todo')





@login_required(login_url="/userlogin")
def delete_todo(request,pk):
    
    m=Todo.objects.filter(id = pk)
    m.delete()
    return redirect('/todo')





import requests
@login_required(login_url="/userlogin")
def books(request):
    if request.method == 'POST':
        form = Dashboardform(request.POST)
        text = request.POST.get('text', '')  # Use get method to avoid KeyError
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)

        # Fix: Call json() method on the response
        answer = r.json()
        
        result_list = []
        for i in range(10):
            volume_info = answer['items'][i].get('volumeInfo', {})
            result_dict = {
                'title': volume_info.get('title', ''),
                'subtitle': volume_info.get('subtitle', ''),
                'description': volume_info.get('description', ''),
                'count': volume_info.get('pageCount', ''),
                'categories': volume_info.get('categories', ''),
                'rating': volume_info.get('pageRating', ''),
                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                'preview': volume_info.get('previewLink', '')
            }

            result_list.append(result_dict)
        
        context = {
            'form': form,
            'results': result_list
        }
        return render(request, 'dashboard/books.html', context)
    else:
        form = Dashboardform()
        context = {'form': form}
        return render(request, "dashboard/books.html", context)



import requests
@login_required(login_url="/userlogin")
def dictionary(request):
    if request.method == "POST":
        form = Dashboardform(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text

        # Correct the method to use requests.get
        r = requests.get(url)

        answer = r.json()
        
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,  # Include the audio information in the context
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': ''
            }
        return render(request, "dashboard/dictionary.html", context)
    else:
        form = Dashboardform()
        context = {'form': form}
        return render(request, 'dashboard/dictionary.html', context)



@login_required(login_url="/userlogin")
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = Dashboardform(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,"dashboard/wiki.html",context)
    else:
        form = Dashboardform()
        context = {'form':form}
    return render(request,"dashboard/wiki.html",context)



def conversion(request):
    context = {'input': False, 'form': ConversionForm()}  # Initialize context with default values
    
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        measurement_value = request.POST.get('measurement', None)  # Use get method with a default value

        if measurement_value == 'length':
            measurement_form = ConversionLengthForm()
            context.update({'m_form': measurement_form, 'input': True})
            
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = request.POST['input']
                answer = ''
                
                if input_value and int(input_value) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input_value} yard = {int(input_value) * 3} foot'
                    elif first == 'foot' and second == 'yard':
                        answer = f'{input_value} foot = {int(input_value) / 3} yard'
                
                context.update({'answer': answer})
        
        elif measurement_value == 'mass':
            measurement_form = ConversionMassForm()
            context.update({'m_form': measurement_form, 'input': True})
            
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = request.POST['input']
                answer = ''
                
                if input_value and int(input_value) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input_value} pound = {int(input_value) * 0.453592} kilogram'
                    elif first == 'kilogram' and second == 'pound':
                        answer = f'{input_value} kilogram = {int(input_value) * 2.20462} pound'
                
                context.update({'answer': answer})
    
    return render(request, "dashboard/conversion.html", context)







@login_required(login_url="/userlogin")
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)  # Corrected 'User' to 'user'
    
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False

    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False

    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todos_done': todos_done
    }

    return render(request, "dashboard/profile.html", context)





from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def register(request):
    if request.method == 'GET':
        return render(request, 'dashboard/register.html')
    else:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        conformpassword = request.POST['conformpassword']

        if name == "" or password == "" or conformpassword == "":
            context = {'msg': 'Field is not empty'}
            return render(request, 'dashboard/register.html', context)

        elif password != conformpassword:
            context = {'msg': 'Password should be the same'}
            return render(request, 'dashboard/register.html', context)
        else:
            u = User.objects.create(username=name, email=email)
            u.set_password(password)
            u.save()
            
            # Redirect to the login page
            return redirect('/userlogin')



def userlogin(request):
    if request.method == 'GET':
        return render(request, "dashboard/userlogin.html")
    else:
        name = request.POST['name']
        password = request.POST['password']

        u = authenticate(username=name, password=password)
        if u is not None:
            auth_login(request, u)  # Use auth_login instead of login
            return redirect('/')
        else:
            error_message = "Incorrect username or password. Please try again."
            return render(request,'dashboard/userlogin.html',{'error_message': error_message})
        
        
def userlogout(request):
    logout(request)
    return  redirect ('/')






def forgot(request,pk):
    if request.method == 'GET':
        m = User.objects.filter(id = pk)
        
        context = {}
        
        context ['data']= m
        
        return render(request,'dashboard/forgot.html',context)
    
    else:
        name = request.POST['name']
        password = request.POST['password']
        
        
        m = User.objects.filter(id = pk)
        m.update(name=name,password=password,)
        return redirect('/userlogin')

