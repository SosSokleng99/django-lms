from typing import Any
from django.db.models.query import QuerySet


from .models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }


    return render(request, 'index.html', context=context)

from django.views import generic # Import generic view classes


class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin ,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o')
            .order_by('due_back')
        )

from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksAllListView(PermissionRequiredMixin ,generic.ListView):

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    permission_required = 'catalog.can_marked_return'

    def get_queryset(self):

        return(
            BookInstance.objects.filter(status__exact = 'o').order_by('due_back')
        )

from django.contrib.auth.decorators import login_required, permission_required
from catalog.forms import RenewBookForm


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

import datetime

@login_required
@permission_required('catalog.can_marked_return', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            #process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renew_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))
    
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renew_date': proposed_renewal_date})
    
    context = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy


#Author's View: CreateView, UpdateView, and DeleteView all these class under Edit Class
class AuthorUpdateView(PermissionRequiredMixin , UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.change_author'

class AuthorCreateView(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'first_name': 'Mr.'}
    permission_required = 'catalog.create_author'

class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    #To validate that the Author Delete Operation always go success_url
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )







