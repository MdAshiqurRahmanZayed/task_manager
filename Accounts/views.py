from django.shortcuts import render,redirect
from Accounts.models import Account 
from .forms import *
from django.contrib import auth



def register(request):
     if request.method == "POST":
          try:
               form = RegistrationForm(request.POST)
               if form.is_valid():
                         email = form.cleaned_data['email']
                         password = form.cleaned_data['password']
                         username = email.split('@')[0] + '_' + email.split('@')[1].split('.')[0]
                         user = Account.objects.create_user( email=email, username=username, password=password)
                         user.is_active = True
                         user.save()
                        
                         return redirect('login')
          except:
                         return redirect('register')
     else:
          form =  RegistrationForm()
     context = {
          'form':form
     }
     return render(request,'Accounts/register.html',context)


def login(request):
     
     if request.method == "POST":
          
          email = request.POST['email']
          password = request.POST['password']
          print(email,password)
          user = auth.authenticate( email=email, password=password)
          if user is not None:
               auth.login(request,user)
               return redirect('home')
          else:
               return redirect('login')
          
     return render(request,'Accounts/login.html')
