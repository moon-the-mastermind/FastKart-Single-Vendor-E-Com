from django.db import models
from product.models import Product
from django.conf import settings

class ProductReviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = "reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name="product_review")
    is_recommended = models.BooleanField(default=True) 
    review_message = models.TextField(blank=True)

    rating = models.FloatField(default=5.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.user.username}-{self.is_recommended}-{self.rating}"
    
class ReviewImages(models.Model):
    review = models.ForeignKey(ProductReviews, on_delete=models.CASCADE, related_name="review_images")
    image = models.ImageField(null= True, blank= True, upload_to="review_images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




