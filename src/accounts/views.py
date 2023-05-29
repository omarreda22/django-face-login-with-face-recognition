from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.contrib import messages
from twilio.rest import Client
from core.env import config

from .forms import RegisterForm, UserCreationForm
from .detection import FaceRecognition
from .tasks import send_email

User = get_user_model()
faceRecognition = FaceRecognition()


def accounts_home(request):
    context = {}
    return render(request, "home.html", context)


def accounts_register(request):
    form = UserCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.save()
        face_id = new_user.id  
        phone_number = new_user.phone_number

        # Face Recognition
        faceRecognition.faceDetect(face_id)
        faceRecognition.trainFace()
        
        # Send SMS Message
        if phone_number is not None:
            account_sid = config('PHONE_ACCOUNT_SID', default=None)
            auth_token = config('PHONE_AUTH_TOKEN', default=None)
            client = Client(account_sid, auth_token)
            message = client.messages \
                            .create(
                                body="Hello there.",
                                from_=config("PHONE_FROM", default=None),
                                to=f'+20{phone_number}'
                            )
        
        # Send Email
        _title = f"Hello {new_user.username}"
        email = new_user.email
        title = _title

        send_email.delay(title, email)

        return redirect("accounts:login")

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)


def accounts_login_page(request):
    return render(request, "accounts/login.html", {})


def accounts_login(request):
    face_id = faceRecognition.recognizeFace()
    
    try:
        user = get_object_or_404(User, id=face_id) 
        # if user is not None:
        login(request, user)
        return redirect("accounts:home")
    except:
        messages.error(request, "You don't have an account, Create new account")
        return redirect("accounts:register")


def accounts_logout(request):
    logout(request)
    return redirect("accounts:login")