# Importamos el módulo 'models' de Django, que nos permite definir modelos de base de datos.
from django.db import models

# Definimos una clase llamada 'Categoria' que hereda de 'models.Model'.
class Categoria(models.Model):
    # Creamos un campo de texto con una longitud máxima de 200 caracteres para almacenar el nombre de la categoría.
    name = models.CharField(max_length=200)

    # Creamos un campo de fecha y hora que se actualizará automáticamente cuando se cree una nueva instancia.
    created = models.DateTimeField(auto_now_add=True)

    # Creamos un campo de fecha y hora que se actualizará automáticamente cada vez que se modifique la instancia.
    updated = models.DateTimeField(auto_now=True)

    # Clase 'Meta' que define metadatos para el modelo.
    class Meta:
        verbose_name = 'Categoria'  # Nombre singular para este modelo en el administrador de Django.
        verbose_name_plural = 'Categorias'  # Nombre plural para este modelo en el administrador de Django.

    # Método que devuelve una representación legible en cadena de esta instancia.
    def __str__(self):
        return self.name

# Definimos una clase llamada 'Producto' que hereda de 'models.Model'.
class Producto(models.Model):
    # Creamos una relación ForeignKey con el modelo 'Categoria'. Esto establece una relación demuchos a uno
    category = models.ForeignKey(Categoria, on_delete=models.RESTRICT)

    # Creamos un campo de texto con una longitud máxima de 200 caracteres para almacenar el nombre del producto.
    name = models.CharField(max_length=200)

    # Creamos un campo de texto largo para almacenar la descripción del producto, que puede ser nulo.
    description = models.TextField(null=True)

    # Creamos un campo decimal para almacenar el precio del producto con un máximo de 9 dígitos y 2 decimales.
    price = models.DecimalField(max_digits=9, decimal_places=2)

    # Creamos un campo booleano que indica la disponibilidad del producto, con valor predeterminado 'True'.
    availability = models.BooleanField(default=True)

    # Definimos un campo "imagen" de tipo ImageField que almacenará la imagen del producto.
    # El parámetro "upload_to='productos'" indica que las imágenes se guardarán en la carpeta "productos" del directorio de medios.
    # Los parámetros "null=True, blank=True" permiten que el campo sea opcional y pueda estar vacío.
    image = models.ImageField(upload_to='productos', null=True, blank=True)

    # Creamos un campo de fecha y hora que se actualizará automáticamente cuando se cree una nueva instancia.
    created = models.DateTimeField(auto_now_add=True)

    # Creamos un campo de fecha y hora que se actualizará automáticamente cada vez que se modifique la instancia.
    updated = models.DateTimeField(auto_now=True)

    # Clase 'Meta' que define metadatos para el modelo.
    class Meta:
        verbose_name = 'Producto'  # Nombre singular para este modelo en el administrador de Django.
        verbose_name_plural = 'Productos'  # Nombre plural para este modelo en el administrador de Django.

    # Método que devuelve una representación legible en cadena de esta instancia.
    def __str__(self):
        return self.name

