from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from . forms import CustomUserCreationForm, LoginForm
from .models import CustomUser, UserProfile
from .utils import send_verification_email, send_password_reset_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator



def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(request, user)
            
            messages.info(request, "Verification link was sent. Check Your email.")
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
                if user.is_verified:
                    login(request, user)
                    messages.success(request, "Login Success")
                    return redirect("profile", slug = user.profile.slug)
                else:
                    messages.error(request, "You're not verified yet. Please Verify your email.")
                    send_verification_email(request, user)
                    messages.info(request, "Verification link was sent. Check Your email.")

            else:
                messages.error(request, "Invalid Username or Password")
            
    else:
        form = LoginForm()

    return render(request, "authsystem/login.html", {"form" : form} )

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


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

     
def verify_email(request, uidb64, token):
    try:
        pk = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(id = pk)
    except (ValueError, TypeError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, "Verification Successful. Redirecting to login page.")
        return redirect("login")
    else:
        messages.error(request, "Link Expired")
        return redirect("signup")
    
def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try :
            user = CustomUser.objects.get(email = email)
            print(user.username)
        except CustomUser.DoesNotExist as e:
            user = None
            messages.error(request, "No user found.")
            return redirect("reset-password")
        
        send_password_reset_email(request, user)
        messages.info(request, "Link was sent to your email. Check it for verify.")
        return redirect("login")
    return render(request, "authsystem/forgot.html")

def verify_password_reset_email(request, uidb64, token):
    pk = urlsafe_base64_decode(uidb64).decode()

    try: 
        user = CustomUser.objects.get(id = pk)

    except (CustomUser.DoesNotExist, TypeError, ValueError, OverflowError, NameError, IndexError) as e :
        user = None
        messages.error(request, f"User Doesn't exists. {e}")
    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()

        return redirect("newpassword")

def new_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        user = request.user
        user.set_password(password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Password changes successfully.")
        return redirect("profile",user.profile.slug)
    return render(request, "authsystem/newpassword.html")


        
