from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language#импорт моделей из файла models.py 
"""далее идет вызов функции admin.site.register(), для регистрации каждой модели"""
# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)

class BooksInline(admin.TabularInline):
    model = Book

# Определение класса администратора
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]


# Регистрация класса администратора с соответствующей моделью
admin.site.register(Author, AuthorAdmin)

"""Вполне логично получить и информацию о книге, и информацию о конкретных копиях, зайдя на страницу детализации.
Вы можете это сделать, объявив inlines, и указав тип TabularInline (горизонтальное расположение) или  
StackedInline (вертикальное расположение, так же как и в модели по умолчанию). Вы можете добавить  BookInstance информацию
в подробное описание  Book , добавив строки, представленные ниже и распологающиеся рядом с  BookAdmin """
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# Регистрация классыа администратора для Book с помощью декоратора
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


# Регистрация класса администратора для BookInstance с помощью декоратора
@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )