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

    def test_editar_precio_libro(self):
        libro_editar = BookList.objects.get(id=1)
        nuevo_precio = libro_editar.price + 10
        libro_editar.price = nuevo_precio
        libro_editar.save()
        self.assertEqual(libro_editar.price, nuevo_precio,msg="Se edito el precio correctamente")

    def test_editar_title_libro(self):
        libro_editar = BookList.objects.get(id=1)
        nuevo_title = "Prueba"
        libro_editar.title  = nuevo_title
        libro_editar.save()
        self.assertEqual(libro_editar.title, nuevo_title,msg="Se edito el titulo correctamente")

    def test_editar_author_libro(self):
        libro_editar = BookList.objects.get(id=1)
        nuevo_author= "Lucio Arias"
        libro_editar.author  = nuevo_author
        libro_editar.save()
        self.assertEqual(libro_editar.author, nuevo_author,msg="Se edito el autor correctamente")

    def test_buscar_libro(self):
        libro = BookList.objects.get(id=1)
        self.assertIn(libro,BookList.objects.all(),msg="El libro existe")

    def test_libro_sin_precio(self):
        libro = BookList.objects.get(id=1)
        self.assertNotEqual(libro.price,None,msg="El libro si posee precio")

    def test_eliminar_libro(self):
        libro_eliminar = BookList.objects.get(id=1)
        libro_eliminar.delete()
        self.assertNotIn(libro_eliminar,BookList.objects.all(),msg="Se elimino el libro correctamente")


    #   pass


class ViewsTestCase(TestCase):

    # Prueba de una vista.
    def test_index_view(self):
        # response = self.client.get(reverse('index', args=[self.userName]))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    #def test_create_view(self):
    #    response = self.client.get(reverse('create'))
    #    self.assertEqual(response.status_code, 200)
    #   self.assertTemplateUsed(response, '')

    def test_add_view(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')
    #   pass

    # def test_delete_view(self):
    #   pass

    def test_edit_view(self):
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
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

    def test_calcular_subtotal_carrito(self):
        libros = BookList.objects.all()
        carrito = [libros[0],libros[1]]
        msj , subtotal = calcularSubTotalCarrito(carrito)
        msj_esperado = 'El subtotal es: $' + '170'
        self.assertEqual(msj_esperado, msj)

    def test_buscar_libros_autor():
        nombre = "Fire & Ice III"
        msj , subtotal = buscarLibrosPorAutor(nombre)
        msj_esperado = 'Se encontraron 1 resultados'
        self.assertEqual(msj_esperado, msj)