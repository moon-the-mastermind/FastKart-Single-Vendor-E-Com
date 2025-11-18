from django.contrib.auth.forms import UserCreationForm
from django import forms
from . models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]
        labels = {
            "first_name" : "First Name",
            "Last_name" : "Last Name",
            "email" : "yourmail@example.com",
            "username" : "Username",
            "password1" : "Strong Password",
            "password2" : "Confirm Password",
            


        }
        widgets = {
            "first_name" : forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "First Name",
                "name" : "first_name",
                "id" : "first_name"
                
            }),

            "last_name" : forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Last Name",
                "name" : "last_name",
                "id" : "last_name"
                
            }),
            
            "email" : forms.EmailInput(attrs={
                "class" : "form-control",
                "placeholder" : "yourmail@example.com",
                "name" : "email",
                "id" : "email"
                
            }),

            "username" : forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "Username",
                "name" : "username",
                "id" : "username"
                
            }),

          
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Strong Password',
            "name" : "password1",
            'id': 'password1'
        })
        self.fields["password1"].label = "Strong Password"

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            "name" : "password2",
            'id': 'password2'
        })
        self.fields["password2"].label = "Confirm Password"

class LoginForm(forms.Form):

    email = forms.EmailField(
        label= "yourmail@example.com",
        widget= forms.EmailInput(attrs={
            "class" : "form-control",
            "placeholder" : "yourmail@example.com",
            "name" : "email",
            "id" : "email",
        })
    )

    password = forms.CharField(
        label= "Password",
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            "name" : "password",
            'id': 'password'
        })
    )
        
    