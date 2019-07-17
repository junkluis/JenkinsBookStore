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
        book = BookList.objects.get(price=90)
        book.title= "Snake"
        book.save(update_fields=["title"])
        self.assertEqual("Snake",book.title)
    
    def test_eliminar_libro(self):
        book = BookList.objects.get(title="Fire & Ice")
        book.delete()
        bookalter = BookList.objects.filter(title="Fire & Ice")
        result = False
        if result :
            result = True
        self.assertEqual(False,result)
        

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
                                        "title": 'Test',
                                        "price": 120,
                                        "author": "Richard Robayo Zapata"
                                    })
        self.assertEqual(response.status_code, 302)

    def test_update_view(self):
        response = self.client.get(
            reverse('update', args=(1,)),
            {
                "title": 'Test',
                "price": 180,
                "author": "Richard Robayo"
            })
        self.assertEqual(response.status_code, 302)


    def test_add_view(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')

    def test_delete_view(self):
        response = self.client.get(reverse('delete', args=(1, )))
        self.assertEqual(response.status_code, 302)

    def test_edit_view(self):
        response = self.client.get(reverse("edit", args=(1, )))
        self.assertEqual(response.status_code, 200)


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

    def test_calcular_subcarrito(self):
        books = BookList.objects.all()
        mensajes,subt = calcularSubTotalCarrito(books)
        subtotal_espera = 210
        self.assertEqual(subtotal_espera,subt)

    def test_buscar_Libros_Xautor(self):
        msj_espera = 'No se encontraron resultados'
        msj, libros = buscarLibrosPorAutor('Richard Robayo')
        self.assertEqual(msj_espera,msj) 
        
