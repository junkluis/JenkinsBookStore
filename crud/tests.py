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
        nuevos_datos_del_libro = ["La pareja inolvidable", 56, "Luis Zuniga"]
        nuevo_libro = BookList.objects.create(title=nuevos_datos_del_libro[0],
                        price=nuevos_datos_del_libro[1],
                        author=nuevos_datos_del_libro[2])
        
        libro_a_editar = BookList.objects.first()
        
        libro_a_editar.title=nuevos_datos_del_libro[0]
        libro_a_editar.price=nuevos_datos_del_libro[1]
        libro_a_editar.author=nuevos_datos_del_libro[2]
        #self.assertEqual(nuevos_datos_del_libro[0], libro_a_editar.title)
        #self.assertEqual(nuevos_datos_del_libro[1], libro_a_editar.price)
        #self.assertEqual(nuevos_datos_del_libro[2], libro_a_editar.author)
        self.assertEqual(nuevo_libro.title, libro_a_editar.title)
        self.assertEqual(nuevo_libro.price, libro_a_editar.price)
        self.assertEqual(nuevo_libro.author, libro_a_editar.author)

    # def test_eliminar_libro(self):
       

    def test_buscar_libro(self):
        libro_buscado = BookList.objects.first()
        campos_esperados = ["Fire & Ice", 90, "Luis Zuniga"]
        self.assertEqual(campos_esperados[0], libro_buscado.title)
        self.assertEqual(campos_esperados[1], libro_buscado.price)
        self.assertEqual(campos_esperados[2], libro_buscado.author)

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
        #response = self.client.get(reverse('/'))
        #self.assertEqual(response.status_code, 200)
        pass

    #def test_add_view(self):
        #response = self.client.post()

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
        res = calcularSubTotalCarrito(carrito)
        self.assertEqual(msj_esperado, res[0])

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