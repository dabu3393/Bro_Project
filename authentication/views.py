from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from bro import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try another username.")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")

        if User.objects.filter(email=email):
            user = User.objects.get(username = email)
            user.username = username
            user.set_password(pass1)

            user.save()


        messages.success(request, "Your account has been successfully created")

        # Welcome Email

        subject = "Welcome to BRO!"
        message = "Hello " + fname + "!! \nWelcome to BRO! You should recieve another email from us asking to confirm your email."
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('home')




    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/signin.html")

        else:
            messages.error(request, "The user name and/or password is incorrect")


def permission(request):

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        referred = request.POST['referred']
        sports = request.POST['sports']

        myuser = User.objects.create_user(email)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.email = email

        myuser.save()

        subject = "New BRO User Request"
        message = "Form Information...\n\nName: " + fname + " " + lname + "\n\nEmail: " + email + "\n\nReferred By: " + referred + "\n\nFavorite Sports Team: " + sports + "\n\nFROM,\nBRO"
        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        return redirect('successful')

    return render(request, "authentication/permission.html")



def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')


def successful(request):
    return render(request, "authentication/successful.html")
