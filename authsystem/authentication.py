from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib import messages

class EmailBackend(ModelBackend):
    def authenticate(self, request, email = None, password = None, **kwargs):
        CustomUser = get_user_model()
        try:
            user = CustomUser.objects.get(email = email)
            if user.check_password(password):
                return user
            else:
                return None
        except CustomUser.DoesNotExist as e:
            return None
    


            

        
        