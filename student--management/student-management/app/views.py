from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StudentForm
from .models import Student


# Create your views here.

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username Already Taken')
            return redirect('register')
        
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.save()
        messages.success(request,'Account Created Successfully')
        return redirect('register')
    return render(request,'register.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            messages.error(request,'Invalid Username')
            return redirect('login')
        
        user = authenticate(username = username , password = password)
        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('login')
        else:
            login(request,user)
            return redirect('add')
        
    
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_student(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            x = form.save(commit=False)
            x.user = request.user  # Set the user to the currently logged-in user
            x.save()
            return redirect('show')
    else:
        pass
    return render(request, 'add.html', {'form': form})

@login_required(login_url='login')
def showview(request):
    stu = Student.objects.filter(user = request.user)
    return render(request,'show.html',{'stu':stu})

def student_edit(request,id):
    data = Student.objects.get(id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST,instance=data)
        if form.is_valid():
            x = form.save(commit=False)
            x.user = request.user
            x.save()
            return redirect('show')
        else:
            pass
    form = StudentForm(instance=data)
    return render(request,'add.html',{'form':form})

def student_remove(request,id):
    data = Student.objects.get(id=id)
    data.delete()
    return redirect('show')

