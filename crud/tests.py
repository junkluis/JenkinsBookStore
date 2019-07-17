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
	    titulo = "Festin de Cuervos"
	    libro = BookList.objects.get(title=titulo)
	    libro.author = "John Cuesta"
	    libro.save(update_fields=['author'])
	    self.assertEqual(libro.author, "John Cuesta")
	#   pass


    def test_eliminar_libro(self):
	    titulo = "Festin de Cuervos"
	    libro = BookList.objects.get(title=titulo)
	    libro.delete()
	    eliminado = True
	    existe_libro = BookList.objects.filter(title=titulo)
	    if existe_libro:
		    eliminado = False
        self.assertEqual(True, eliminado)
	#   pass

    
    def test_buscar_libro(self):
        titulo = "Fire & Ice"
        libro = BookList.objects.get(title=titulo)
        self.assertEqual(libro.title, titulo)
    #   pass


    def test_libro_sin_precio(self):
        info_libro = ["Festin de Cuervos", 0, "Luis Zuniga"]
        BookList.objects.create(title=info_libro[0],
                                price=info_libro[1],
                                author=info_libro[2])
        libro = BookList.objects.get(title="Festin de Cuervos")
        self.assertEqual(libro.price, 0)
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
            {"title": "1984", "price": 50, "author": "George Orwell"}
        )
        self.assertEqual(response.status_code, 302)
    #   pass


    def test_update_view(self):
        info_libro = ["Festin de Cuervos", 40, "Luis Zuniga"]
        BookList.objects.create(title=info_libro[0],
                                price=info_libro[1],
                                author=info_libro[2])
        libro_actualizado = {"title": "Drácula", "price": 70, "author": "Bram Stoker"}
        response = self.client.get(reverse("update", args=(1,)), libro_actualizado)
        self.assertEqual(response.status_code, 302)
    #   pass


    def test_add_view(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')
    #   pass


    def test_delete_view(self):
        response = self.client.get(reverse('delete', args=(1, )))
        self.assertEqual(response.status_code, 302)
    #   pass


    def test_edit_view(self):
        response = self.client.get(reverse("edit", args=(1, )))
        self.assertEqual(response.status_code, 200)
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


    def carrito_sin_libros(self):
        libro_de_prueba = None
        carrito = []
        respuesta = agregarLibroAlCarrito(libro_de_prueba, carrito)
        respuesta_prueba = 'Err: No hay ningun libro'
        self.assertEqual(respuesta_prueba, respuesta)
        #   pass


    def carrito_subtotal(self):
        libros = BookList.objects.all()
        subtotal = calcularSubTotalCarrito(libros)
        subtotal_prueba = 210
        self.assertEqual(subtotal_prueba, subtotal)
        #   pass


    def carrito_subtotal_no_libros(self):
        carrito = 0
        respuesta, subtotal = calcularSubTotalCarrito(carrito)
        respuesta_prueba = 'No tiene libros en el carrito.'
        subtotal_prueba = 0
        self.assertEqual(respuesta_prueba, respuesta)
        self.assertEqual(subtotal_prueba, subtotal)
        #   pass


    def carrito_lleno(self):
        carrito = [BookList.objects.all()]
        libro_prueba = BookList.objects.create(title="Libro de Prueba", price=60, author="John Cuesta")
        respuesta_prueba = 'Solo puede ingresar hasta ' \
                'un maximo de 10 Libros ' \
                'al carrito'
        for i in range(10):
            respuesta = agregarLibroAlCarrito(libro_prueba, carrito)
            
        self.assertEqual(respuesta_prueba, respuesta)
        #   pass




