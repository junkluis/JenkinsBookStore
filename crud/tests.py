"""Definition of tests for app crud"""
from django.test import TestCase
from django.urls import reverse
from .models import BookList
from .views import *

# Create your tests here.


class BookTestCase(TestCase):
    """Test Case class for book CRUD"""

    def setUp(self):
        """ Initial setup for test case"""
        # Creamos un libro para las pruebas
        BookList.objects.create(title="Fire & Ice",
                                price=90,
                                author="Luis Zuniga")

    def test_crear_nuevo_libro(self):
       """Test create new book"""
       lista_libros = len(BookList.objects.all())
       info_libro = ["Festin de Cuervos", 40, "Luis Zuniga"]
       BookList.objects.create(title=info_libro[0],
                               price=info_libro[1],
                               author=info_libro[2])
       lista_libros_actualizado = len(BookList.objects.all())
       self.assertEqual(lista_libros + 1, lista_libros_actualizado)

    # def test_editar_libro(self):
    #   pass

    # def test_eliminar_libro(self):
    #   pass

    # def test_buscar_libro(self):
    #   pass

    # def test_libro_sin_precio(self):
    #   pass


class ViewsTestCase(TestCase):
    """Test Views for app"""

    # Prueba de una vista.
    def test_index_view(self):
        """Test index template rendering"""
        # response = self.client.get(reverse('index', args=[self.userName]))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    # def test_create_view(self):
    #     data = {
    #         "author": "Pablo Coehllo",
    #         "price": 100,
    #         "title": "No SE"
    #     }

    #     response = self.client.post(reverse('create'), data,
    #                                     content_type='json')
    #     self.assertEqual(response.status_code, 200)


    # def test_add_view(self):
    #   pass

    # def test_delete_view(self):
    #   pass

    # def test_edit_view(self):
    #   pass


class FunctionsTestCase(TestCase):
    """TestCaste for model instance functions"""

    def setUp(self):
        """ Initial setup for test case """
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
        """ Add to cart book """
        carrito = []
        libros = BookList.objects.all()
        msj = agregar_libro_al_carrito(libros[0], carrito)
        msj_esperado = 'Libro: Fire & Ice fue agregado al carrito'
        self.assertEqual(msj_esperado, msj)

    def test_calcular_subtotal(self):
        """ Test subtotal calculation"""
        subtotal_esperado = 90 + 80 + 40
        msj_esperado = 'El subtotal es: ${}'.format(subtotal_esperado)

        libros = BookList.objects.all()

        msj, subtotal = calcular_subtotal_carrito(libros)
        self.assertEqual(subtotal_esperado, subtotal)
        self.assertEqual(msj_esperado, msj)

    def test_calcular_subtotal_carrito_vacio(self):
        """ Subtotal esperado para carrito vacio"""
        subtotal_esperado = 0
        msj_esperado = 'No tiene libros en el carrito.'

        libros = []

        msj, subtotal = calcular_subtotal_carrito(libros)
        self.assertEqual(subtotal_esperado, subtotal)
        self.assertEqual(msj_esperado, msj)

    def test_buscar_libro_autor(self):
        """Busqueda de libro por autor existente"""
        total = 3
        msj_esperado = 'Se encontraron {} resultados'.format(total)
        msj, libros = buscar_libros_por_autor("Luis Zuniga")

        self.assertEqual(msj_esperado, msj)
        self.assertEqual(total, libros.count())

