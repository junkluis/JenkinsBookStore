"""Definition of tests for app crud"""
from django.test import TestCase
from django.urls import reverse
from .models import BookList
from .views import *

# Create your tests here.

import json

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

    def test_editar_libro(self):
        """ Prueba de actualizar campos"""
        update_fields = ['title', 'price']
        update_data = ['Earth II', 200]

        book = BookList.objects.first()
        book.title = 'Earth II'
        book.price = 200
        book.save(update_fields=update_fields)

        book = BookList.objects.first()
        self.assertEqual(update_data[0], book.title)
        self.assertEqual(update_data[1], book.price)

    def test_eliminar_libro(self):
        cantidad_actual = BookList.objects.all().count()
        cantidad_esperada = cantidad_actual - 1

        book = BookList.objects.first()
        book.delete()

        self.assertEqual(cantidad_esperada, BookList.objects.all().count())

    def test_buscar_libro(self):

        params_busqueda = {
            'title':"Fire & Ice",
            'price': 90,
            'author': "Luis Zuniga"
        }
        found = True
        try:
            book = BookList.objects.get(**params_busqueda)
        except BookList.DoesNotExist:
            found = False

        self.assertTrue(found)
        self.assertEqual(params_busqueda['title'], book.title)
        self.assertEqual(params_busqueda['price'], book.price)
        self.assertEqual(params_busqueda['author'], book.author)

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

    def test_create_view(self):
        """Test create view and redirection """
        data = {
             "author": "Pablo Coehllo",
             "price": 100,
             "title": "No SE"
        }

        response = self.client.post(reverse('create'), data) 
        self.assertEqual(response.status_code, 302)
        created = True
        try:
            book = BookList.objects.get(**data)
        except BookList.DoesNotExist:
            created = False

        self.assertTrue(created)


    def test_add_view(self):
        """Render add form for book"""
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')

    # def test_delete_view(self):
    #   pass

    def test_edit_view(self):
        """Test rendering and template context for editting"""
        book_to_edit = BookList.objects.create(title="Fire & Ice",
                                                price=90,
                                                author="Luis Zuniga")
        response = self.client.get(reverse('edit', args=[book_to_edit.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
        self.assertEqual(book_to_edit, response.context['books'])


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

    def test_elemento_inesperado_en_carrito(self):
        """Non BookList instance in method test"""
        book = "not a book"
        msj_esperado = 'Err: No hay ningun libro'

        carrito = []
        msj = agregar_libro_al_carrito(book, carrito)
        self.assertEqual(msj_esperado, msj)

    def test_demasiados_libros_en_carrito(self):
        """Test for trying to add more than 10 books to cart"""
        for i in range(11):
            title="Bears are Cool".format(i)
            libro_prueba = BookList.objects.create(title=title,
                                                    price=(i + 1) * 10,
                                                    author="Alex Arktos")
        carrito = []
        msj_esperado = 'Solo puede ingresar hasta un maximo de 10 ' +\
                        'Libros al carrito'
        msj = ''
        books = list(BookList.objects.filter(author="Alex Arktos"))[:11]

        for i in range(11):
            msj = agregar_libro_al_carrito(books[i], carrito)

        self.assertEqual(11, len(books))
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

