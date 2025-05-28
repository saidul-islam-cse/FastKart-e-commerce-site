from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms
from .import utils
from django.utils.http import urlsafe_base64_decode
from . import models
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_signup(request):
    if request.method == "POST":
        form = forms.CustomUserRegistrationForms(request.POST)
        if form.is_valid():
            user = form.save()
            utils.send_verification_email(request, user)
            messages.info(request, "We have sent you an verification email")
            return redirect('login')
    return render(request, "accounts/signup.html")

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = models.CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, models.CustomUser.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, "Your email has been verified successfully.")
        return redirect('login')
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect('signup')
    
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if not user:
            messages.error(request, "Invalid email or password.")
        elif not user.is_verified:
            messages.error(request, "Your email is not verified yet.")
        else:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect("profile")
    
    return render(request, "accounts/login.html")
@login_required
def user_logout(request):
    logout(request)
    return redirect("home")


def user_dashboard(request):
    user = request.user

    if request.method == "POST":
        user.email = request.POST.get("email", user.email)
        user.mobile = request.POST.get("mobile", user.mobile)
        user.address_line_1 = request.POST.get("address_line_1", user.address_line_1)
        user.address_line_2 = request.POST.get("address_line_2", user.address_line_2)
        user.city = request.POST.get("city", user.city)
        user.postcode = request.POST.get("postcode", user.postcode)
        user.country = request.POST.get("country", user.country)

        user.save()
        return redirect("profile")
    context = {"user_info" : user}
    return render(request, "accounts/profile.html", context)


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = models.CustomUser.objects.get(email=email)
        except models.CustomUser.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("password-reset")
        utils.send_password_reset_email(request, user)
        messages.info(
            request, "We have sent you an email with password reset instructions"
        )
        return redirect("login")
    return render(request, "accounts/forgot.html")


def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = models.CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, models.CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        login(request, user)
        return redirect("new-password")
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect("login")
@login_required   
def set_new_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        user = request.user
        user.set_password(password)
        user.save()
        messages.success(request, "Password updated successfully.")
        return redirect("profile")
    return render(request, "accounts/new-password.html")