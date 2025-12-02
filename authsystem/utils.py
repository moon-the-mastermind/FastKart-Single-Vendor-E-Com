from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    scheme = "https" if request.is_secure() else "http"
    current_site = get_current_site(request)
    verification_url = f"{scheme}://{current_site.domain}/user/verify/{uid}/{token}"

    email_subject = "Please Verify Your Account."
    email_body = render_to_string("authsystem/verification_email.html",{
        "user" : user,
        "verification_url" : verification_url,

    })

    email = EmailMessage(
        subject= email_subject,
        body= email_body,
        from_email= settings.DEFAULT_FROM_EMAIL,
        to= [user.email]
    )

    email.content_subtype = "html"
    
    try :
        email.send()
    except Exception as e:
        print(f"failed to send email : {e}")

def send_password_reset_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    scheme = "https" if request.is_secure() else "http"
    current_site = get_current_site(request)
    password_reset_url = f"{scheme}://{current_site.domain}/user/reset-password-confirm/{uid}/{token}"

    email_subject = "Reset Your Password."
    email_body = render_to_string("authsystem/password_reset_email.html",{
        "user" : user,
        "password_reset_url" : password_reset_url,

    })
    email = EmailMessage(
        subject=email_subject,
        body= email_body,
        from_email= settings.DEFAULT_FROM_EMAIL,
        to= [user.email]
    )
    email.content_subtype = "html"
    try :
        email.send()
    except Exception as e:
        print(f"failed to send email : {e}")


