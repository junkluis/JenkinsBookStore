from django.shortcuts import render, redirect, HttpResponse

from .models import BookList

# Create your views here.

def index(request):
    books = BookList.objects.all()
    context = {
        'books': books
    }
    return render(request, 'index.html', context)

def create(request):
    print(request.POST)
    title = request.GET['title']
    price = request.GET['price']
    author = request.GET['author']
    book_details = BookList(title=title, price=price, author=author)
    book_details.save()
    return redirect('/')


def add_book(request):
    return render(request, 'add_book.html')



def delete(request, id):
    books = BookList.objects.get(pk=id)
    books.delete()
    return redirect('/')

def edit(request, id):
    books = BookList.objects.get(pk=id)
    context = {
        'books': books
    }
    return render(request, 'edit.html', context)


def update(request, id):
    books = BookList.objects.get(pk=id)
    books.title = request.GET['title']
    books.price = request.GET['price']
    books.author = request.GET['author']
    books.save()
    return redirect('/')


def agregarLibroAlCarrito(libro, carrito):
    msj = ''

    if(isinstance(libro, BookList)):
        if(len(carrito) < 10):
            carrito.append(libro)
            msj = 'Libro: '.libro.title.' fue agregado al carrito'
        else:
            msj = 'Solo puede ingresar hasta un maximo de 10 Libros al carrito'
    else:
        msj = 'Err: No hay ningun libro'

    return msj



def calcularSubTotalCarrito(carrito):
    msj = ""
    subtotal = 0

    if(carrito != 0):
        for libro in carrito:
            subtotal += libro.price
        msj = 'El subtotal es: $'.str(subtotal)
    else:
        msj = 'No tiene libros en el carrito'
        subtotal = 0

    return (msj, subtotal)



def buscarLibrosPorAutor(nombre_autor):
    msj = ""
    todosLosLibros = BookList.objects.filter(author=nombre_autor)

    if(len(todosLosLibros) > 0):
        msj = 'Se encontraron '.str(len(todosLosLibros)).' resultados'
    else:
        msj = 'No se encontraron resultados'

    return (msj, todosLosLibros)
    