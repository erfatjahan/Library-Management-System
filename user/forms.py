from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user.models import GENDER, UserAccountModel, UserAddressModel



class UserRegistrationForm(UserCreationForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER)
    street1 = forms.CharField(max_length=50)
    street2 = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'birthday', 'gender', 'street1', 'street2', 'city', 'postal_code', 'country']
    
    def save(self, commit=True):
        our_user = super().save(commit=False) # ami database e data save korbo na ekhn
        if commit == True:
            our_user.save() # user model e data save korlam
            birthday = self.cleaned_data.get('birthday')
            gender = self.cleaned_data.get('gender')
            street1 = self.cleaned_data.get('street1')
            street2 = self.cleaned_data.get('street2')
            postal_code = self.cleaned_data.get('postal_code')
            city = self.cleaned_data.get('city')
            country = self.cleaned_data.get('country')
            
            UserAddressModel.objects.create(
                user = our_user,
                postal_code = postal_code,
                country = country,
                city = city,
                street1 = street1,
                street2 = street2,
            )
            UserAccountModel.objects.create(
                user = our_user,
                gender = gender,
                birthday = birthday,
                account = 17600 + our_user.id
            )
        return our_user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })
            
            
class AddMoneyForm(forms.Form):
    amount = forms.DecimalField(label='Enter Amount to Deposit', min_value=0)



class ChangeUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']