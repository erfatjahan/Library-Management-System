from django.db import models
from django.contrib.auth.models import User
from books.models import BookModel

# Create your models here.
GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)


class UserAccountModel(models.Model):
    user = models.OneToOneField(User, related_name="accounts", on_delete=models.CASCADE)
    account = models.IntegerField()
    birthday = models.DateField()
    gender = models.CharField(max_length=30, choices=GENDER)
    initial_deposit_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    
class UserAddressModel(models.Model):
    user = models.OneToOneField(User, related_name="address", on_delete=models.CASCADE)
    street1 = models.CharField(max_length=50)
    street2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=50) 
    
    

class PurchaseModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    Book = models.ForeignKey(BookModel,on_delete=models.CASCADE, null=True, blank=True)
    isBorrowed = models.BooleanField(default=True, null = True, blank = True)

    def __str__(self):
        return f"{self.user.first_name}  borrowed : {self.Book.title}"
    
    
