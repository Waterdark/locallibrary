from django.shortcuts import render # render() - функция, которая генерирует HTML-файлы при помощи шаблонов
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic

# Create your views here.

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применен по умолчанию.
    # Количество посещений этого представления, подсчитанное в переменной сеанса (session).
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    # Отрисовка HTML-шаблона index.html с данными внутри 
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books':num_books,
                'num_instances':num_instances,
                'num_instances_available':num_instances_available,
                'num_authors':num_authors,
                'num_visits':num_visits, 
                },
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10 #поле для пострантчного вывода данных (если боее 10, остальное выводится на следующих страницах)

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5 

class AuthorDetailView(generic.DetailView):
    model = Author