from email import message
from lib2to3.pgen2.tokenize import generate_tokens
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from bro import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.core.mail import EmailMessage, send_mail

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

        user = User.objects.get(username = email)
        user.username = username
        user.set_password(pass1)
        user.is_active = False

        if User.objects.filter(email=email):
            user.save()


        messages.success(request, "Your account has been successfully created")

        # Welcome Email

        subject = "Welcome to BRO!"
        message = "Hello " + username + "!! \nWelcome to BRO! You should recieve another email from us asking to confirm your email."
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm your email for BRO"
        message2 = render_to_string('email_confirmation.html', {
            'name': user.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        })

        email = EmailMessage(
            email_subject,
            message2,
            settings. EMAIL_HOST_USER,
            [email],
        )
        email.fail_silently = True
        email.send()

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

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, "authentication/signin.html")
    else:
        return render(request, 'activation_failed.html')
