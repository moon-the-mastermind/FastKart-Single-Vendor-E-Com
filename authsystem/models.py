from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
class UserProfile(models.Model):

    GENDER_CHOICE = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Others")
    ]

    COUNTRY_CHOICES = [
        ("UK", "United Kingdom"),
        ("BD", "Bangladesh"),
        ("IN", "India"),
        ("PK", "Pakistan"),
        ("FR", "France"),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to="userprofile")
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=100)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, default="BD")
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username, allow_unicode=True)
            slug = base_slug
            counter = 1

            while UserProfile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


