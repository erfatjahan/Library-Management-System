from django.contrib import admin
from user.models import PurchaseModel, UserAccountModel, UserAddressModel

# Register your models here.
admin.site.register(UserAccountModel)
admin.site.register(UserAddressModel)
admin.site.register(PurchaseModel)