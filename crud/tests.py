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
        cantidad_anterior_libros = len(BookList.objects.all())
        info_nuevo_libro = ["Festin de Cuervos", 40, "Luis Zuniga"]
        BookList.objects.create(title=info_nuevo_libro[0],
                                price=info_nuevo_libro[1],
                                author=info_nuevo_libro[2])
        cantidad_libros_actual = len(BookList.objects.all())

        self.assertEqual(cantidad_anterior_libros+1, cantidad_libros_actual)

    def test_add_book(self):
        cambios = False
        add_book(None)

        self.assertEqual(False, cambios)


    def test_editar_libro(self):         
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
        libro_a_eliminar = BookList.objects.get(pk=1)
        delete("", 1)
        confirmacion = False
        libro_a_eliminar.delete()
        print(libro_a_eliminar)
        if libro_a_eliminar is None:
            confirmacion = True
        
        self.assertEqual(confirmacion, False)

    def test_buscar_libro(self):
        libro_buscado = BookList.objects.first()
        campos_esperados = ["Fire & Ice", 90, "Luis Zuniga"]
        self.assertEqual(campos_esperados[0], libro_buscado.title)
        self.assertEqual(campos_esperados[1], libro_buscado.price)
        self.assertEqual(campos_esperados[2], libro_buscado.author)

    def test_libro_sin_precio(self):
        libro_nuevo = BookList.objects.create(title="Las manzanas",
                                price=0,
                                author="Clara Alcazar L.")

        self.assertEqual(0, libro_nuevo.price)    



class ViewsTestCase(TestCase):

    # Prueba de una vista.
    def test_index_view(self):
        # response = self.client.get(reverse('index', args=[self.userName]))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_create_view(self):
        libro = {"title":"La pareja inolvidable", "price": 50, "author":"Wellington Martinez"}
        respuesta = self.client.get(reverse('create'), libro)
        self.assertEqual(respuesta.status_code, 302)

    def test_add_view(self):
        respuesta = self.client.get(reverse('add_book'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'add_book.html')

    def test_delete_view(self):
        respuesta = self.client.get("/delete/1")
        self.assertEqual(respuesta.status_code, 301)

    def test_edit_view(self):
        respuesta = self.client.get("/edit/1")
        self.assertEqual(respuesta.status_code, 301)

    def test_update_view(self):
        respuesta = self.client.get("/update/1")
        self.assertEqual(respuesta.status_code, 301)

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
    
    def test_agregar_libro_a_carrito_lleno(self):  
        carrito = []      
        libros = BookList.objects.all()
        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
            carrito.append(BookList.objects.first())

        msj = agregarLibroAlCarrito(libros[0], carrito)
        msj_esperado = 'Solo puede ingresar hasta un maximo de 10 Libros al carrito'
        self.assertEqual(msj_esperado, msj)

    def test_no_agregar_libro_a_carrito(self):
        libro_falso = 0
        carrito = []
        msj = 'Err: No hay ningun libro'
        msj_esperado = agregarLibroAlCarrito(libro_falso, carrito)
        self.assertEqual(msj, msj_esperado)

    def test_calcular_subtotal_carrito(self):
        msj_esperado = 'El subtotal es: $90'        
        carrito = []
        libro = BookList.objects.first()
        agregarLibroAlCarrito(libro, carrito)
        res,valor = calcularSubTotalCarrito(carrito)
        print('El subtotal es: $90')
        self.assertEqual(msj_esperado, res)

    def test_calcular_subtotal_carrito_vacio(self):
        msj_esperado = 'No tiene libros en el carrito.'        
        carrito = 0
        res = calcularSubTotalCarrito(carrito)
        self.assertEqual(msj_esperado, res[0])

    def test_buscar_libros_por_autor(self):
        autor = 'Luis Zuniga'
        msj_esperado = msj = 'Se encontraron 3 resultados'
        res = buscarLibrosPorAutor(autor)
        self.assertEqual(res[0], msj_esperado)

    def test_buscar_libros_por_autor_no_existente(self):
        autor = 'Wellington Martinez'
        msj_esperado = msj = 'No se encontraron resultados'
        res = buscarLibrosPorAutor(autor)
        self.assertEqual(res[0], msj_esperado)        