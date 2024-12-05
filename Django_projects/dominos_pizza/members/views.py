from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .forms import RegisterForm
from django.contrib import messages

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