from django.shortcuts import render # render() - функция, которая генерирует HTML-файлы при помощи шаблонов
from .models import Book, Author, BookInstance, Genre, Language #импорт перечисленных моделей из models.py
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin



# Create your views here.

def index(request):
    """Функция отображения для домашней страницы сайта."""
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применен по умолчанию.
    num_genre = Genre.objects.count()
    # Количество посещений этого представления, подсчитанное в переменной сеанса (session).
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    # num_visits = 0 # обнулятор посещений 
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
                'num_genre': num_genre,
                },
    )

class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 5 

class GenreDetailView(generic.DetailView):
    model = Genre
    paginate_by = 5

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10 #поле для пострантчного вывода данных (если более 10, остальное выводится на следующих страницах)

class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 5

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5 

class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 5

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Общий вид на основе класса, в котором перечислены книги, переданные в аренду текущему пользователю.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Общий вид на основе класса со списком всех книг, взятых в долг. Отображается только пользователям с разрешением can_mark_returned."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')