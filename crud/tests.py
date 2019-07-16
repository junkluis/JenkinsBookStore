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

    def test_eliminar_libro(self):
        libros = BookList.objects.all()
        lista_libros = len(libros)
        libros[0].delete()
        lista_libros_actualizado = len(BookList.objects.all())
        self.assertEqual(lista_libros-1, lista_libros_actualizado)

    # def test_buscar_libro(self):
    #   pass

    # def test_libro_sin_precio(self):
    #   pass


class ViewsTestCase(TestCase):

    def setUp(self):
        # Creamos un libro para las pruebas
        BookList.objects.create(title="Fire & Ice",
                                price=90,
                                author="Luis Zuniga")

    # Prueba de una vista.
    def test_index_view(self):
        # response = self.client.get(reverse('index', args=[self.userName]))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_create_view(self):
        response = self.client.get(
            '/create', {'title': 'How to program Java', 'price': 20,
                        'author': 'Deitel'})
        self.assertEqual(response.status_code, 301)

    def test_add_view(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')

    def test_edit_view(self):
        libros = BookList.objects.all()
        response = self.client.get(f'/edit/{libros[0].pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')

    def test_update_view(self):
        libros = BookList.objects.all()
        response = self.client.get(
            f'/update/{libros[0].pk}', {'title': 'How to program Java',
                                        'price': 20, 'author': 'Deitel'})
        self.assertEqual(response.status_code, 301)

    def test_delete_view(self):
        libros = BookList.objects.all()
        response = self.client.get(f'/delete/{libros[0].pk}/')
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
        msj = agregar_libro_al_carrito(libros[0], carrito)
        msj_esperado = 'Libro: Fire & Ice fue agregado al carrito'
        self.assertEqual(msj_esperado, msj)

    def test_agregar_carrito_max(self):
        carrito = [0] * 10
        libros = BookList.objects.all()
        msj = agregar_libro_al_carrito(libros[0], carrito)
        msj_esperado = 'Solo puede ingresar hasta un maximo de 10 Libros al carrito'
        self.assertEqual(msj_esperado, msj)

    def test_agregar_carrito_err(self):
        carrito = []
        msj = agregar_libro_al_carrito('Un libro', carrito)
        msj_esperado = 'Err: No hay ningun libro'
        self.assertEqual(msj_esperado, msj)

    def test_calcular_subtotal_carrito_valido(self):
        carrito = BookList.objects.all()
        msj, subtotal = calcular_subtotal_carrito(carrito)
        msj_esperado = 'El subtotal es: $210'
        subtotal_esperado = 210
        self.assertEqual(msj_esperado, msj)
        self.assertEqual(subtotal_esperado, subtotal)

    def test_calcular_subtotal_carrito_vacio(self):
        carrito = 0
        msj, subtotal = calcular_subtotal_carrito(carrito)
        msj_esperado = 'No tiene libros en el carrito.'
        subtotal_esperado = 0
        self.assertEqual(msj_esperado, msj)
        self.assertEqual(subtotal_esperado, subtotal)
