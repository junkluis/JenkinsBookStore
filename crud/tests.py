from django.test import TestCase
from django.urls import reverse
from .models import BookList
from .views import *

# Create your tests here.

class BookTestCase(TestCase):

    def setUp(self):
        # Creamos un libro para las pruebas
        BookList.objects.create(title="Fire & Ice",
                                price=90,
                                author="Luis Zuniga")

    def test_crear_nuevo_libro(self):

        lista_libros = len(BookList.objects.all())
        info_libro = ["Festin de Cuervos", 40, "Luis Zuniga"]
        BookList.objects.create(title=info_libro[0],
                                price=info_libro[1],
                                author=info_libro[2])
        lista_libros_actualizado = len(BookList.objects.all())

        self.assertEqual(lista_libros+1, lista_libros_actualizado)

    def test_editar_libro(self):
        info_libro = ["Festin de Cuervos", 40, "Luis Zuniga"]
        BookList.objects.create(title=info_libro[0],
                                price=info_libro[1],
                                author=info_libro[2])
        precioOld = BookList.objects.get(title="Festin de Cuervos").price
        book = BookList.objects.get(tittle="Festin de Cuervos")
        book.price = 100
        self.assertEqual(precioOld+60, book.price)

    """def test_eliminar_libro(self):
        info_libro = ["Festin de Cuervos", 40, "Luis Zuniga"]
        BookList.objects.create(title=info_libro[0],
                                price=info_libro[1],
                                author=info_libro[2])
        lista_libros = len(BookList.objects.all())
        book = BookList.objects.get("Festin de Cubervos")
        del book
        self.assertEqual(lista_libros-1, len(BookList.objects.all()))"""

    def test_buscar_libro_exitoso(self):
        info_libro = ["Mil Horas 2", 40, "Jonathan Parrales"]
        BookList.objects.create(title=info_libro[0],
                                price=info_libro[1],
                                author=info_libro[2])
        mensaje = buscarLibrosPorAutor("Jonathan Parrales")
        libro = BookList.objects.filter(author="Jonathan Parrales")
        self.assertEqual(tuple('Se encontraron 1 resultados', libro), tuple(mensaje))
    
    def test_buscar_libro_fallido(self):
        info_libro = ["Mil Horas 3", 40, "Jonathan Parrales"]
        BookList.objects.create(title=info_libro[0],
                                price=info_libro[1],
                                author=info_libro[2])
        libro = BookList.objects.filter(author="Jonathan Neira")
        mensaje = buscarLibrosPorAutor("Jonathan Neira")
        self.assertEqual(tuple('No se encontraron resultados', libro), tuple(mensaje))

    def test_calcular_subtotal_carrito(self):
        info_libro = ["Mil Horas 4", 40, "Jonathan Parrales"]
        BookList.objects.create(title=info_libro[0],
                                price=info_libro[1],
                                author=info_libro[2])
        libros = BookList.objects.all()
        suma = 0
        for x in libros:
            suma += x.price
        preciosTotal = calcularSubTotalCarrito(BookList.objects.all())
        self.assertEquals(tuple("El subtotal es: $"+str(suma), suma), tuple(preciosTotal))


class ViewsTestCase(TestCase):

    # Prueba de una vista.
    def test_index_view(self):
        # response = self.client.get(reverse('index', args=[self.userName]))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    # def test_create_view(self):
    #   pass

    # def test_add_view(self):
    #   pass

    # def test_delete_view(self):
    #   pass

    # def test_edit_view(self):
    #   pass


class FunctionsTestCase(TestCase):

    def setUp(self):
        # Creamos un libro para las pruebas
        libro_prueba = BookList.objects.create(title="Fire & Ice",
                                               price=90,
                                               author="Luis Zuniga")
        libro_prueba = BookList.objects.create(title="Fire & Ice II",
                                               price=80,
                                               author="Luis Zuniga")
        libro_prueba = BookList.objects.create(title="Fire & Ice III",
                                               price=40,
                                               author="Luis Zuniga")

    # Prueba de una vista.
    def test_agregar_carrito(self):
        carrito = []
        libros = BookList.objects.all()
        msj = agregarLibroAlCarrito(libros[0], carrito)
        msj_esperado = 'Libro: Fire & Ice fue agregado al carrito'
        self.assertEqual(msj_esperado, msj)
