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
        book.title = "software"
        book.save(update_fields=["title"])
        self.assertEqual("software", book.title)


    def test_eliminar_libro(self):
        
        BookList.objects.filter(title="Festin de Cuervos").delete()
        book = BookList.objects.filter(title="Festin de Cuervos")
        exito = False
        if book:
            exito = True
        self.assertEqual(False, exito)

    def test_buscar_libro(self):
       
        libro = BookList.objects.get(title="Festin de Cuervos")
        self.assertEqual("Festin de Cuervos", libro.title)


       





class ViewsTestCase(TestCase):

    # Prueba de una vista.
    def test_index_view(self):
        # response = self.client.get(reverse('index', args=[self.userName]))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

   

   

   


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



    def test_agregar_carrito2(self):
        comprar_libros = []
        libros = BookList.objects.all()
        for i in range(10):       
            agregarLibroAlCarrito(libros[0], comprar_libros)
        msj = agregarLibroAlCarrito(libros[0], comprar_libros)
        msj_esperado = ('Solo puede ingresar hasta un maximo de 10 Libros al carrito')
        self.assertEqual(msj_esperado, msj)





    def test_calcular_subtotal_carrito(self):
        libros = BookList.objects.all()
        msj, subtotal = calcularSubTotalCarrito(libros)
        subtotal_esperado = 210
        self.assertEqual(subtotal_esperado, subtotal)

    def test_calcular_subtotal_carrito2(self):
        libros = 0
        mensaje, subtotal = calcularSubTotalCarrito(libros)
        self.assertEqual(mensaje, 'No tiene libros en el carrito.')
        self.assertEqual(subtotal, 0)


    def test_buscar_Libros(self):
        esperado = 'No se encontraron resultados'
        mensaje, todoslibros = buscarLibrosPorAutor('Cristiano Ronaldo')
        self.assertEqual(esperado, mensaje)

    def test_buscar_Libros2(self):
        esperado = 'Se encontraron 3 resultados'
        mensaje, todoslibros = buscarLibrosPorAutor("Luis Zuniga")
        self.assertEqual(esperado,"Se encontraron 3 resultados")