from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductReviews



@receiver([post_save, post_delete], sender = ProductReviews)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    reviews = product.reviews.all()
    total_reviews = reviews.count()

    if total_reviews > 0:

        avg_rating = sum(review.rating for review in reviews if review.rating is not None) / total_reviews
        avg_rating = max(0, min(avg_rating, 5))

        recommended_count = reviews.filter(is_recommended= True).count()
        recommended_percentage = (recommended_count / total_reviews) * 100
        recommended_percentage = max(0, min(recommended_percentage, 100))

    else:
        avg_rating = 0.00
        recommended_percentage = 0.00

    product.average_rating = round(avg_rating, 2)
    product.total_review = total_reviews
    product.recommended_percentage = round(recommended_percentage, 2)

    product.save(update_fields = ["average_rating", "recommended_percentage", "total_review"])
