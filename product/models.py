from django.db import models
from django.utils.text import slugify
from django.conf import settings
# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank= True)
    description = models.TextField(null = True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            counter = 1

            while Categories.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="product")

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True) #auto generate
    description = models.TextField(null = True)
    sku = models.CharField(max_length=100)
    size = models.CharField(max_length=50, null=True)
    color = models.JSONField(default=list, null= True, blank=True)
    in_stock = models.IntegerField() 
    # is_available = models.BooleanField(default=False) #auto generate
    price = models.FloatField()
    discount_percent = models.FloatField()
    # total_price = models.FloatField(blank = True) #auto generate
    average_rating = models.FloatField(default=100.00)
    recommended_percentage = models.FloatField(default=100.00, null=True)
    total_review = models.PositiveIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price (self):
        return self.price - self.price * self.discount_percent/100
    
    @property
    def is_available(self):
        is_available = False
        if self.in_stock > 0:
            return is_available == True
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug    
            count = 1
            
            while Product.objects.filter(slug = slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug

        #discount validation
        if self.discount_percent < 0:
            self.discount_percent = 0

        elif self.discount_percent > 100:
            self.discount_percent = 100
        
        
        


        super().save(*args, **kwargs)

class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="product_comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.comment[:50]}"
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = "product_image")
    image = models.ImageField(null=True, blank=True, upload_to="product_image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - image"