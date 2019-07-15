from django.test import TestCase
from .models import BookList

# Create your tests here.
class BookTestCase(TestCase):

    def setUp(self):
    	#Creamos un libro para las pruebas
    	BookList.objects.create(title="Fire & Ice", price=90, author="Luis Zuniga")

    def test_crear_nuevo_libro(self):
    	lista_libros = len(BookList.objects.all())
    	print(lista_libros)
    	info_libro = ["Festin de Cuervos", 40, "Luis Zuniga"]
    	BookList.objects.create(title=info_libro[0], price=info_libro[1], author=info_libro[2])
    	lista_libros_actualizado = len(BookList.objects.all())

    	self.assertEqual(lista_libros+1 , lista_libros_actualizado)

    #def test_editar_libro(self):
    #	pass

    #def test_eliminar_libro(self):
    #	pass

    #def test_buscar_libro(self):
    #	pass

    #def test_libro_sin_precio(self):
    #	pass
