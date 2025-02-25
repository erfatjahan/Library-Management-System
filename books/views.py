from django.views.generic import DetailView
from django.views.generic import ListView
from user.models import PurchaseModel
from category.models import CategoryModel
from .models import BookModel
from django.shortcuts import render
from django.views import View
from .forms import CommentForm

def all_books(request, category_slug=None):
    books = BookModel.objects.all()
    category = CategoryModel.objects.all()
    if category_slug:
        cat_type = CategoryModel.objects.filter(slug=category_slug).first()
        if cat_type:
            books = BookModel.objects.filter(category=cat_type)

    return render(request, 'book_list.html', {'books': books, 'categories': category})


class ShowDetails(DetailView):
    model = BookModel
    template_name = 'details.html'
    context_object_name = 'books'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        comments = book.comments.all()
        comment_form = CommentForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form

        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        book = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post_book = book  # Associate the comment with the book
            new_comment.save()
        
        return self.get(request, *args, **kwargs)