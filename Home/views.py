from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
def index(request):
   return render(request, 'index.html')

@login_required
def mission(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    return render(request, 'mission.html')

def work(request):
   return render(request, 'work.html')

def team(request):
   return render(request, 'team.html')

def contact(request):
   if request.method == "POST":
      name = request.POST.get('name')
      email = request.POST.get('email')
      phone = request.POST.get('phone')
      msg = request.POST.get('msg') 

      # save kaise kre(object bna rhe phir save kr rhe hai)
      c = Contact(name=name, email=email, phone= phone, msg=msg)
      c.save()
      return redirect("/contact")
   
   data = Contact.objects.order_by('-name') # list of object aa gya

   return render(request, 'contact.html',{'data': data}) 


def signupView(request):

    if request.method == "POST":
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        userName = request.POST.get('userName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        user = User.objects.create_user(userName, email, password)
        user.first_name =  firstName
        user.last_name = lastName
        user.save()
        return redirect('/login')

    return render(request, 'signup.html')

def loginView(request):
    if request.method == "POST":
        userName = request.POST.get('userName')
        password = request.POST.get('password')
        user = authenticate(request, username=userName, password=password)

        if user is not None:
            # 2. Start the session
            login(request, user)
            return redirect('/home') 
        else:
            # 3. Handle failed login
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutView(request):
   logout(request)
   return render(request, "index.html")