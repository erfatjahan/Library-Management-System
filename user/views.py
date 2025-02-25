from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import FormView
from user.forms import ChangeUserForm, UserRegistrationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from user.models import UserAccountModel
from user.forms import AddMoneyForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from books.forms import CommentForm
from .models import BookModel, PurchaseModel
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# mail send korar function
def send_mail_to_user(user, subject, template, added_amount=None):
    # Retrieve the user account
    user_account = UserAccountModel.objects.get(user=user)
    
    # Calculate the total balance
    total_balance = user_account.balance
    
    # If an added amount is provided, update the balance
    if added_amount is not None:
        user_account.balance += added_amount
        total_balance = user_account.balance
        user_account.save()
    
    message = render_to_string(template, {
        'user': user,
        'amount': added_amount,  # Pass the added amount to the template
        'total_balance': total_balance  # Pass the total balance to the template
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


# Create your views here.
class RegistrationView(FormView):
    template_name = 'registration_form.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('registration')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
@login_required  
def userLogout(request):
    logout(request)
    return redirect('home')

# @login_required
# def add_money(request):
#     form = AddMoneyForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         amount = form.cleaned_data['amount']
#         user_account = UserAccountModel.objects.get(user=request.user)
#         user_account.balance += amount
#         user_account.save()
#         msg = messages.success(request, f"{amount} added successfully")
#         #send mail notification
#         send_mail_to_user(request.user, "Successfully Added Money", "addMoneyMail.html")
#         return render(request, 'home.html', {'messages': msg})
    
#     return render(request, 'add_money.html', {'form': form})

@login_required
def add_money(request):
    form = AddMoneyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']
        user_account = UserAccountModel.objects.get(user=request.user)
        user_account.balance += amount
        user_account.save()
        msg = messages.success(request, f"{amount} added successfully")
        
        # Send mail notification with added amount
        send_mail_to_user(request.user, "Successfully Added Money", "addMoneyMail.html", added_amount=amount)
        return render(request, 'home.html', {'messages': msg})
    
    return render(request, 'add_money.html', {'form': form})




@login_required
def profile_view(request):
    purchased_books = PurchaseModel.objects.filter(user=request.user.accounts.user, isBorrowed=True)
    context = {
        'books': purchased_books,
    }
    return render(request, 'profile.html', context)





#update profile
class EditProfileView(LoginRequiredMixin, FormView):
    template_name = 'update_profile.html'
    form_class = ChangeUserForm
    success_url = reverse_lazy('profile')  # Replace with your actual success URL
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profile Updated Successfully')
        return super().form_valid(form)
    




class BuyBookView(View):
    def get(self, request, book_id):
        # books = BookModel.objects.all()
        book = get_object_or_404(BookModel, pk=book_id)
        user_account = request.user.accounts  # Assuming this gets the related UserAccountModel
        user = user_account.user  # Retrieve the related User instance

        comments = book.comments.all()
        
        if user_account.balance >= book.price and book.quantity > 0:
            user_account.balance -= book.price
            book.quantity -= 1
            user_account.save()
            book.save()
            purchase = PurchaseModel.objects.create(user=user, Book=book)# purchase model a Book variable ache tai ekhaen book likhlam
            messages.success(request, f"You have successfully purchased a book.")
            send_mail_to_user(request.user, "Book Purchase Success", "purchase.html")
            
            # comment_page_url = reverse('comment_page', kwargs={'id': book.id})  
            # return redirect(comment_page_url)
            return render(request, 'comment_page.html', {'book': book, 'comments': comments})
        else:
            messages.warning(request, "You cannot purchase a book with insufficient balance.")
            send_mail_to_user(request.user, "Book Purchase Failed", "purchaseFail.html")
            return redirect('all_books')
    def post(self, request, book_id):
        book = get_object_or_404(BookModel, pk=book_id)
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post_book = book  # Associate the comment with the book
            new_comment.save()
            
            comments = book.comments.all()  # Fetch all comments related to the book
            
            # Render comment_page.html with book details and comments
            # return render(request, 'comment_page.html', {'book': book, 'comments': comments})
            return redirect('home')

 
 
 
    


class ReturnBookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(BookModel, pk=book_id)
        user_account = request.user.accounts  # related_name accounts ache tai 
        user = user_account.user  # Retrieve the related User instance

        if user_account.balance >= book.price and book.quantity > 0:
            user_account.balance += book.price
            book.quantity += 1
            user_account.save()
            book.save()

            # return korar time a get PurchaseModel.objects.get() use korle martro ekta book return korte parbo tai 'filter' use krola jate onek book return kora jai
            purchases = PurchaseModel.objects.filter(user=user, Book=book)
            for purchase in purchases:
                purchase.isBorrowed = False  # boi return hobe, tai false korlam karon profile a only isBorrowed=True hole tobe profile list a dekhabe
                purchase.save()

            messages.success(request, f"You have successfully returned a book.")
            send_mail_to_user(request.user, "Book Returned Success", "returnMail.html")
            return redirect('profile')
        else:
            messages.warning(request, "You cannot return the book at the moment.")
            send_mail_to_user(request.user, "Book Return Failed", "returnFail.html")
            return redirect('all_books')


