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
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)