from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

@login_required
def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Libros disponibles (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # El 'all()' esta implícito por defecto.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context= {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_visits':num_visits,
    }
    )
    
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'my_book_list'   # su propio nombre para la lista como variable de plantilla
    template_name = 'book_list.html'  # Especifique su propio nombre/ubicación de plantilla
    def get_context_data(self, **kwargs):
        book_list = Book.objects.all()
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context = {'book_list':book_list}
        return context

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    paginate_by = 10
    
class BookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    context_object_name = 'my_bookinstance_list'   # su propio nombre para la lista como variable de plantilla
    template_name = 'bookinstance_list.html'  # Especifique su propio nombre/ubicación de plantilla
    def get_context_data(self, **kwargs):
        bookinstance_list = BookInstance.objects.all()
        # Call the base implementation first to get the context
        context = super(BookInstanceListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context = {'bookinstance_list':bookinstance_list}
        return context

class BookInstanceDetailView(LoginRequiredMixin, generic.DetailView):
    model = BookInstance
    paginate_by = 10
  
class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    context_object_name = 'my_author_list'   # su propio nombre para la lista como variable de plantilla
    template_name = 'author_list.html'  # Especifique su propio nombre/ubicación de plantilla
    def get_context_data(self, **kwargs):
        author_list = Author.objects.all()
        # Call the base implementation first to get the context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context = {'author_list':author_list}
        return context

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    paginate_by = 10
    
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Vista genérica basada en clases que enumera los libros prestados al usuario actual.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='a').order_by('due_back')
 
class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='a').order_by('due_back') 
    
@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    #initial={'date_of_death'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = ['title','author','summary','isbn','genre' ]

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

class BookInstanceCreate(CreateView):
    model = BookInstance
    fields = ['book','imprint','due_back','borrower','status' ]

class BookInstanceUpdate(UpdateView):
    model = BookInstance
    fields = ['imprint','due_back','borrower','status' ]

class BookInstanceDelete(DeleteView):
    model = BookInstance
    success_url = reverse_lazy('bookinstances')