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
        BookList.objects.filter(title="Fire & Ice").update(price=50)
        libro = BookList.objects.get(title="Fire & Ice")
        self.assertEqual(50, libro.price)

    def test_eliminar_libro(self):
        lista_libros = len(BookList.objects.all())
        BookList.objects.filter(title="Fire & Ice").delete()
        lista_libros_actualizado = len(BookList.objects.all())

        self.assertEqual(lista_libros-1, lista_libros_actualizado)

    def test_buscar_libro(self):
        titulo_libro_a_buscar = "Fire & Ice"
        libro = BookList.objects.get(title=titulo_libro_a_buscar)

        self.assertEqual(libro.title, titulo_libro_a_buscar)

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
        form_data = {"title": "1984", "price": 20, "author": "George Orwell"}
        response = self.client.get(reverse('create'), form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')

    def test_add_view(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')

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
