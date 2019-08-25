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
        expected = False
        try:
            edit(None, 1)
            expected = True
        except AssertionError:
            expected = False

        self.assertEqual(expected, True)

    def test_eliminar_libro(self):
        expected = False
        try:
            delete(None, 1)
            expected = True
        except AssertionError:
            expected = False

        self.assertEqual(expected, True)

    def test_buscar_libro(self):
        expected_msj = 'Se encontraron 1 resultados'
        msj, books = buscarLibrosPorAutor("Luis Zuniga")

        self.assertEqual(msj, expected_msj)

    def test_libro_sin_precio(self):
        expected_msj = 'No se encontraron resultados'
        msj, books = buscarLibrosPorAutor("Wellington Martinez")

        self.assertEqual(msj, expected_msj)


class ViewsTestCase(TestCase):

    # Prueba de una vista.
    def test_index_view(self):
        # response = self.client.get(reverse('index', args=[self.userName]))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_create_view(self):
        book = {"title": "Im stronger",
                "author": "Wellington Martinez",
                "price": 100}
        response = self.client.get('/create', book)

        self.assertEqual(301, response.status_code)

    def test_add_view(self):
        response = self.client.get(reverse('add_book'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'add_book.html')

    def test_delete_view(self):
        book = BookList.objects.create(title="La navidad",
                                        price=100, author="Wellington Martinez")
        response = self.client.get(reverse('delete', args=[book.id]))

        self.assertEqual(response.status_code, 302)

    def test_edit_view(self):
        book = BookList.objects.create(title="La navidad",
                                        price=100, author="Wellington Martinez")
        response = self.client.get(reverse('edit', args=[book.id]))

        self.assertEqual(200, response.status_code)

    def test_update_view(self):
        book = BookList.objects.create(title="La navidad",
                                        price=100, author="Wellington Martinez")
        edit_data = {
            "title": book.title,
            "price": 180,
            "author": book.author
        }
        response = self.client.get(reverse('update', args=[book.id]), edit_data)

        self.assertEqual(response.status_code, 302)


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
    
    def test_agregar_carrito_exceso(self):
        car = []
        book = BookList.objects.first()
        expected_msj = 'Solo puede ingresar hasta un maximo de 10 Libros al carrito'
        for i in range(15):
            msj = agregarLibroAlCarrito(book, car)

        self.assertEqual(msj, expected_msj)

    def test_agregar_carrito_no_libro(self):
        car = []
        book = 0
        expected_msj = 'Err: No hay ningun libro'
        msj = agregarLibroAlCarrito(book, car)

        self.assertEqual(msj, expected_msj)

    def test_calcular_subtotal_carrito(self):
        expected_msj = 'El subtotal es: $130'
        car = []
        car.append(BookList.objects.first())
        car.append(BookList.objects.last())
        msj, subtotal = calcularSubTotalCarrito(car)

        self.assertEqual(expected_msj, msj)

    def test_calcular_subtotal_carrito_vacio(self):
        expected_msj = 'No tiene libros en el carrito.'
        car = 0
        msj, subtotal = calcularSubTotalCarrito(car)

        self.assertEqual(msj, expected_msj)