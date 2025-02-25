from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from category.models import CategoryModel

# Create your models here.
class BookModel(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    quantity = models.IntegerField(default=0, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.category} -> {self.title}"
    
    
class CommentModel(models.Model):
    name = models.CharField(max_length=30)
    post_book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
        
    def __str__(self):
        return f"Commented by {self.name}"