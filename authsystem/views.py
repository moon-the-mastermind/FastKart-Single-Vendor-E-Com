from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import CustomUserCreationForm, LoginForm
from .models import CustomUser, UserProfile

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            user = form.save()

            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, email = email, password = password)
            if user:
                messages.success(request, "Success ! Logging In")
                login(request, user)
                return redirect("profile")
            else:
                messages.error(request, "User Doesn't Found")
        else:
            messages.error(request, "Check the form and try again")
    else:
        form = CustomUserCreationForm()

    return render(request, "authsystem/signup.html", {"form" : form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, email = email, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Success")
                return redirect("profile", slug= request.user.profile.slug)
            else:
                messages.error(request, "Invalid Username or Password")
            
    else:
        form = LoginForm()

    return render(request, "authsystem/login.html", {"form" : form} )

@login_required
def user_logout(request):
    logout(request)
    return redirect("signup")


def user_profile(request, slug):
    user = request.user

    user_profile = UserProfile.objects.get(slug = slug)

    if request.method == "POST":
        user.email = request.POST.get("email", user.email)
        user.username = request.POST.get("username", user.username)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.save()

        user_profile.phone = request.POST.get("mobile", user_profile.phone)
        user_profile.address = request.POST.get("address", user_profile.address)
        user_profile.postal_code = request.POST.get("postal", user_profile.postal_code)
        user_profile.country = request.POST.get("country", user_profile.country)
        user_profile.gender = request.POST.get("country", user_profile.gender)
        user_profile.bio = request.POST.get("bio", user_profile.bio)
        user_profile.save()

    context = {

        "user_info" : user,
        "user_profile" : user_profile
    }
        
    return render(request, "authsystem/user_profile.html", context)