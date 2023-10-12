from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

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

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )

class BookListView(generic.ListView):
    model = Book
    
    # su propio nombre para la lista como variable de plantilla
    context_object_name = 'my_book_list'   
    
    # Consigue 5 libros que contengan el título de guerra.
    #def get_queryset(self):
    #   return Book.objects.filter(title__icontains='war')[:5]
    # Especifique su propio nombre/ubicación de plantilla
    #template_name = 'books/my_arbitrary_template_name_list.html'  
    
    #def get_context_data(self, **kwargs):
    #    # Llame primero a la implementación base para obtener un contexto.
    #    context = super(BookListView, self).get_context_data(**kwargs)
    #    # Obtenga el blog del id y agréguelo al contexto.
    #    context['some_data'] = 'Estos son solo algunos datos'
    #    return context