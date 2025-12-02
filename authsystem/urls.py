from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views

urlpatterns = [
    path("signup/", views.signup, name = "signup"),
    path("login/", views.login_view, name = "login"),
    path("logout/", views.user_logout, name = "logout"),
    path("profile/<str:slug>", views.user_profile, name = "profile"),

    path("verify/<uidb64>/<token>/", views.verify_email, name="verify_email"),
    path("reset-password/", views.password_reset, name= "reset-password"),
    path("reset-password-confirm/<uidb64>/<token>/", views.verify_password_reset_email, name = "verify_password_reset"),
    path("set-password/", views.new_password, name="newpassword")
    
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)