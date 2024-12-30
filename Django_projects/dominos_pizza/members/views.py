from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from .models import Post
from django.contrib.auth import login

def members(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Акаунт створений🎉🎉')
            return redirect('members')
        else:
            messages.error(request,'Перевірте дані🤣')
    else:
        form = RegisterForm()

    return render(request,'register.html',{'form':form})

def show_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts.html',{'posts':posts})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request,user)

            messages.success(request,message="Ви успішно увійшли в акаунт👍👍")
            return redirect('posts')
        else:
            messages.error(request,"Невірні дані🤣🤣")
    else:
        form = LoginForm()
    return render(request,'login.html',{"form":form})