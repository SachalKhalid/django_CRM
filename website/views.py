from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
from .forms import SignUpForm
from .forms import AddRecordForm
# Create your views here.
def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        #Login user
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('Error Logging In - Please Try Again...'))
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('home')

def register_user(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Athunticating the User
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username = username, password = password)
            login(request, user)

            messages.success(request, ('You have Registered!'))
            return redirect('home')
        else:
            messages.success(request, ('Error Registering - Please Try Again...'))
            return redirect('register')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'forms':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)
        return render(request, 'record.html', {'record':record})
    else:
        messages.success(request, ('Please Login to View Customer Record...'))
        return redirect('home.html')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)
        record.delete()
        messages.success(request, ('Record has been Deleted...'))
        return redirect('home')
    else:
        messages.success(request, ('Please Login to View Customer Record...'))
        return redirect('home.html')
    

def add_record(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddRecordForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ('Record has been Added...'))
                return redirect('home')
            else:
                messages.success(request, ('Error Adding Record - Please Try Again...'))
                return redirect('add_record')
        else:
            form = AddRecordForm()
            return render(request, 'add_record.html', {'forms':form})
    else:
        messages.success(request, ('Please Login to Add Customer Record...'))
        return redirect('home.html')
    

def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)
        if request.method == 'POST':
            form = AddRecordForm(request.POST, instance=record)
            if form.is_valid():
                form.save()
                messages.success(request, ('Record has been Updated...'))
                return redirect('home')
            else:
                messages.success(request, ('Error Updating Record - Please Try Again...'))
                return redirect('update_record')
        else:
            form = AddRecordForm(instance=record)
            return render(request, 'update_record.html', {'forms':form})
    else:
        messages.success(request, ('Please Login to Update Customer Record...'))
        return redirect('home.html')
