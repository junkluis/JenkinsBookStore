from django.shortcuts import render, redirect, HttpResponse

from .models import BookList

# Create your views here.


def index(request):
    """List books in front page"""
    books = BookList.objects.all()
    context = {
        'books': books
    }
    return render(request, 'index.html', context)


def create(request):
    """Create book instance"""
    title = request.GET['title']
    price = request.GET['price']
    author = request.GET['author']
    book_details = BookList(title=title, price=price, author=author)
    book_details.save()
    return redirect('/')


def add_book(request):
    """Renders form to add book"""
    return render(request, 'add_book.html')


def delete(request, id):
    """Remove book instance"""
    books = BookList.objects.get(pk=id)
    books.delete()
    return redirect('/')


def edit(request, id):
    """Edit book instance template"""
    books = BookList.objects.get(pk=id)
    context = {
        'books': books
    }
    return render(request, 'edit.html', context)


def update(request, id):
    """Update book instance"""
    books = BookList.objects.get(pk=id)
    books.title = request.GET['title']
    books.price = request.GET['price']
    books.author = request.GET['author']
    books.save()
    return redirect('/')


def agregar_libro_al_carrito(libro, carrito):
    """Adds book to shopping cart"""
    msj = ''

    if isinstance(libro, BookList):
        if len(carrito) < 10:
            carrito.append(libro)
            msj = 'Libro: ' + (libro.title) + ' fue agregado al carrito'
        else:
            msj = 'Solo puede ingresar hasta un maximo de 10 Libros al carrito'
    else:
        msj = 'Err: No hay ningun libro'

    return msj


def calcular_subtotal_carrito(carrito):
    """Get total value sans IVA"""
    msj = ""
    subtotal = 0

    if carrito != 0:
        for libro in carrito:
            subtotal += libro.price
        msj = 'El subtotal es: $'.str(subtotal)
    else:
        msj = 'No tiene libros en el carrito.'
        subtotal = 0

    return (msj, subtotal)


def buscar_libros_por_autor(nombre_autor):
    """Get filtered book list"""
    msj = ""
    todos_los_libros = BookList.objects.filter(author=nombre_autor)

    if todos_los_libros:
        msj = 'Se encontraron ' + str(len(todos_los_libros)) + ' resultados'
    else:
        msj = 'No se encontraron resultados'

    return (msj, todos_los_libros)
