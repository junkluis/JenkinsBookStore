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

    def test_obtener_titulo(self):
        book = BookList.objects.get(price=90)
        tituloEsperado = "Fire & Ice"
        titulo = str(book)
        self.assertEqual(titulo, tituloEsperado)

    def test_crear_nuevo_libro(self):

        lista_libros = len(BookList.objects.all())
        info_libro = ["Festin de Cuervos", 40, "Luis Zuniga"]
        BookList.objects.create(title=info_libro[0],
                                price=info_libro[1],
                                author=info_libro[2])
        lista_libros_actualizado = len(BookList.objects.all())

        self.assertEqual(lista_libros+1, lista_libros_actualizado)

    def test_editar_libro(self):
        book = BookList.objects.get(price=90)
        book.author = "José Luis Massón"
        book.save(update_fields=['author'])
        self.assertEqual(book.author, "José Luis Massón")

    def test_eliminar_libro(self):
        book = BookList.objects.get(price=90)
        book.delete()
        book2 = BookList.objects.filter(price=90)
        self.assertEqual(len(book2), 0)

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
        response = self.client.get(
                                    reverse('create'),
                                    {
                                        "title": 'Prueba',
                                        "price": 90,
                                        "author": "José Massón"
                                    })
        self.assertEqual(response.status_code, 302)

    def test_update_view(self):
        response = self.client.get(
                                    reverse('update', args=(1, )),
                                    {
                                        "title": 'Prueba',
                                        "price": 150,
                                        "author": "José Massón"
                                    })
        self.assertEqual(response.status_code, 302)

    def test_add_view(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')

    def test_delete_view(self):
        response = self.client.get(reverse('delete', args=(1, )))
        self.assertEqual(response.status_code, 302)

    def test_delete_view_correct_data(self):
        book_delete = BookList.objects.create(
                                                title="Prueba Delete",
                                                price=100,
                                                author="Jose Masson")                                              
        response = self.client.get(reverse('delete', args=[book_delete.id]))
        self.assertEqual(response.status_code, 302)

    def test_edit_view(self):
        response = self.client.get(reverse("edit", args=(1, )))
        self.assertEqual(response.status_code, 200)

    def test_edit_view_correct_data(self):
        new_book_edit = BookList.objects.create(
                                                title="Prueba 2",
                                                price=100,
                                                author="Jose Masson")                                
        response = self.client.get(reverse('edit', args=[new_book_edit.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
        self.assertEqual(new_book_edit, response.context['books'])


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

    def test_agregar_carrito_limite_10(self):
        carrito = []
        libros = BookList.objects.all()
        msj_esperado = "Solo puede ingresar hasta "
        msj_esperado += "un maximo de 10 Libros "
        msj_esperado += "al carrito"
        for i in range(11):
            libro = libros[0]
            msj = agregarLibroAlCarrito(libros[0], carrito)
        self.assertEqual(msj, msj_esperado)

    def test_agregar_carrito_libro_incorrecto(self):
        carrito = []
        libro = []
        msj = agregarLibroAlCarrito(libro, carrito)
        msj_esperado = 'Err: No hay ningun libro'
        self.assertEqual(msj, msj_esperado)

    def test_calcular_sub_carrito(self):
        libros = BookList.objects.all()
        msj, subtotal = calcularSubTotalCarrito(libros)
        subtotal_esperado = 210
        self.assertEqual(subtotal_esperado, subtotal)

    def test_calcular_sub_carrito_vacio(self):
        carrito = 0
        msj, subtotal = calcularSubTotalCarrito(carrito)
        msj_esperado = 'No tiene libros en el carrito.'
        subtotal_esperado = 0
        self.assertEqual(subtotal, subtotal_esperado)
        self.assertEqual(msj, msj_esperado)

    def test_buscar_libros_por_autor_no_existente(self):
        msj_esperado = "No se encontraron resultados"
        msj, todosLibros = buscarLibrosPorAutor('José Luis Massón')
        self.assertEqual(msj_esperado, msj)

    def test_buscar_libros_por_autor_existente(self):
        msj_esperado = "Se encontraron 3 resultados"
        msj, todosLibros = buscarLibrosPorAutor('Luis Zuniga')
        self.assertEqual(msj_esperado, msj)
