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
        title = "Nuevo titulo"
        lista_libros = len(BookList.objects.all())
        info_libro = ["Festin de Cuervos", 40, "Luis Zuniga"]
        book = BookList.objects.create(title=info_libro[0],
                                       price=info_libro[1],
                                       author=info_libro[2])
        book.save()
        book.title = title
        book.save()
        self.assertEqual(title, book.title)

#def test_eliminar_libro(self):

#def test_buscar_libro(self):

#def test_libro_sin_precio(self):


class ViewsTestCase(TestCase):

    # Prueba de una vista.
    def test_index_view(self):
        # response = self.client.get(reverse('index', args=[self.userName]))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_create_view(self):
        data = {"title": "dfdf", "price": 40, "author": "dsfd"}
        response = self.client.get(reverse('create'), data)
        self.assertEqual(response.status_code, 302)


    def test_add_view(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')


    def test_delete_view(self):
        response = self.client.get("/delete/1")
        self.assertEqual(response.status_code, 301)


    def test_edit_view(self):
        response = self.client.get("/edit/1")
        self.assertEqual(response.status_code, 301)


    def test_update_view(self):
        response = self.client.get("/update/1")
        self.assertEqual(response.status_code, 301)


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

    def test_agregar_carrito_nuevo(self):
        carrito = []
        libros = BookList.objects.all()
        libro_prueba = BookList.objects.create(title="Libro 1",
                                               price=20,
                                               author="MAuricio Leiton")
        msj = agregarLibroAlCarrito(libro_prueba, carrito)
        msj_esperado = 'Libro: '+(libro_prueba.title)+' fue agregado al carrito'
        self.assertEqual(msj_esperado, msj)

    def test_agregar_carrito_no_libro(self):
        carrito = []
        libros = BookList.objects.all()
        libro_prueba = None
        msj = agregarLibroAlCarrito(libro_prueba, carrito)
        msj_esperado = 'Err: No hay ningun libro'
        self.assertEqual(msj_esperado, msj)

    def test_agregar_carrito_max_libro(self):
        carrito = [BookList.objects.all()]
        libros = BookList.objects.all()
        libro_prueba = BookList.objects.create(title="Libro 1",
                                               price=20,
                                               author="MAuricio Leiton")
        for i in range(10):
            msj = agregarLibroAlCarrito(libro_prueba, carrito)
        msj_esperado = 'Solo puede ingresar hasta un maximo de 10 Libros al carrito'
        self.assertEqual(msj_esperado, msj)

    def test_calcular_subtotal_carrito_vacio(self):
        carrito = []
        msj = calcularSubTotalCarrito(carrito)
        msj_text = 'El subtotal es: $'+str(0)
        msj_esperado = (msj_text, 0)
        self.assertEqual(msj_esperado, msj)

    def test_calcular_subtotal_carrito_nada(self):
        carrito = []
        libro_prueba = BookList.objects.create(title="Libro 1",
                                               price=20,
                                               author="MAuricio Leiton")
        agregarLibroAlCarrito(libro_prueba, carrito)
        msj = calcularSubTotalCarrito(carrito)
        msj_text = 'El subtotal es: $'+str(libro_prueba.price)
        msj_esperado = (msj_text, libro_prueba.price)
        self.assertEqual(msj_esperado, msj)