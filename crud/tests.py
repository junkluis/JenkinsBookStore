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


    # def test_editar_libro(self):
    #   pass  



    # def test_eliminar_libro(self):
    #   pass

    # def test_buscar_libro(self):
    #   pass

    # def test_libro_sin_precio(self):
    #   pass


class ViewsTestCase(TestCase):

    # Prueba de una vista.
    def test_index_view(self):
        # response = self.client.get(reverse('index', args=[self.userName]))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_create_view(self):
        response = self.client.get(reverse('create'), {'title':'new', 'price':50,'author':'alex'})
        self.assertEqual(response.status_code, 302)


    def test_add_view(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')


    def test_update_view(self):
        response = self.client.get('/update/1')
        self.assertEqual(response.status_code, 301)


    def test_delete_view(self):
        response = self.client.get('/delete/1')
        self.assertEqual(response.status_code, 301)


    def test_edit_view(self):
        response = self.client.get('/edit/1')
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
        libro_prueba = BookList.objects.create(title="Fire",
                                               price=90,
                                               author="Alex")
        msj = agregarLibroAlCarrito(libros[0], carrito)
        msj_esperado = 'Libro: '+(libro_prueba.title)+' fue agregado al carrito'
        self.assertEqual(msj_esperado, msj)


    def test_agregar_carrito_else_libro(self):
        carrito = []
        libros = BookList.objects.all()
        libro_prueba = None
        msj = agregarLibroAlCarrito(libro_prueba, carrito)
        msj_esperado = 'Err: No hay ningun libro'
        self.assertEqual(msj_esperado, msj)


    def test_agregar_carrito_libro_maximo(self):
        carrito = [BookList.objects.all()]
        libros = BookList.objects.all()
        libro_prueba = BookList.objects.create(title="Fire",
                                               price=90,
                                               author="Alex")
        for i in range(10):
            msj = agregarLibroAlCarrito(libro_prueba, carrito)
        msj_esperado = 'Solo puede ingresar hasta un maximo de 10 Libros al carrito'
        self.assertEqual(msj_esperado, msj)
