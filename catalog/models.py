from django.db import models
from django.urls import reverse #Используется для генерации URL путем изменения шаблонов URL
import uuid # Требуется для уникальных экземпляров книги

# Create your models here.
class Genre(models.Model):
    """Модель, представляющая жанр книги (например, Фантастика, Non Fiction)."""
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    
    def __str__(self):
        """
        Строка для представления объекта Model (на сайте администратора и т. Д.)
        Метод просто возвращает имя жанра, определенного конкретной записью
        """
        return self.name


"""
Модель книги представляет всю информацию о доступной книге в общем смысле, но не конкретный физический «экземпляр» 
или «копию» для временного использования. Модель использует CharField для представления названия книги и isbn 
(обрати внимание, как isbn указывает свой ярлык как «ISBN», используя первый неименованный параметр, 
поскольку в противном случае ярлык по умолчанию был бы «Isbn»). Модель использует TextField для summary, потому что этот текст, 
возможно, должен быть очень длинным.
"""
class Book(models.Model):
    """Модель, представляющая книгу (но не конкретную копию книги)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Используется внешний ключ, потому что у книги может быть только один автор, но у авторов может быть несколько книг
    # Автор как строка, а не объект, потому что он еще не был объявлен в файле.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField используется потому, что жанр может содержать много книг. Книги могут охватывать многие жанры.
    # Класс Genre (жанр) уже определен, поэтому мы можем указать объект выше.
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        """Строка для представления объекта Model, возвращает названия книг."""
        return self.title
    
    
    def get_absolute_url(self):
        """Возвращает URL для доступа к конкретному экземпляру книги."""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """Создает строку для жанра. Это необходимо для отображения жанра в Admin."""
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'


"""
BookInstance представляет собой определенную копию книги, которую кто-то может брать взаймы, и включает информацию о том, 
доступна ли копия или в какой день она ожидается, «отпечаток» или сведения о версии, а также уникальный идентификатор книги 
в библиотеке
"""
class BookInstance(models.Model):
    """Модель, представляющая конкретную копию книги (то есть, которая может быть заимствована из библиотеки)."""
    #UUIDField используется для поля id, чтобы установить его как primary_key для этой модели
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    # Метаданные модели (Class Meta) используют это поле для упорядочивания записей, когда они возвращаются в запросе.
    # Это значение может быть blank или null (необходимо, когда книга доступна). 
    due_back = models.DateField(null=True, blank=True)

    """
    LOAN_STATUS - кортеж содержащий кортежи пар ключ/значение в последствии передаваемый аргументу выбора (choices в status)
    Значение в key/value паре - это отображаемое значение, которое пользователь может выбрать, а ключи - это значения,
    которые фактически сохраняются, если выбрана опция
    """
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    # Это CharField, который определяет список choice/selection
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        

    def __str__(self):
        """Строка для представления объекта Model"""
        return '%s (%s)' % (self.id, self.book.title)


class Author(models.Model):
    """Модель, представляющая автора."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    def get_absolute_url(self):
        """Возвращает URL для доступа к конкретному экземпляру автора."""
        return reverse('author-detail', args=[str(self.id)])
    

    def __str__(self):
        """Строка для представления объекта Model."""
        return '%s, %s' % (self.last_name, self.first_name)

class Language(models.Model):
    """Модель, представляющая язык (например, английский, французский, японский и т. Д.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """Строка для представления объекта Model (на сайте администратора и т. Д.)"""
        return self.name