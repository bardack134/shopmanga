# Importa el módulo models de Django
from django.db import models

# Importa el modelo User de django.contrib.auth.models
from django.contrib.auth.models import User

from autenticacion.models import Cliente
from web.models import Producto


"""CUANDO EL USUARIO HACE EL PEDIDO PASAMOS TODA LA INFORMACION DEL CARRITO GUARDADA EN LA SESION A LA BASE DE DATOS, ES LO QUE NORMALMENTE SE HACE CUANDO UN USUARIO PROCESA EL CARRITO"""

# Define el modelo Pedido, esta vista corresponde es al estado del pedido, cuando el cliente hace el pedido
class Pedido(models.Model):
    
    # Define una relación ForeignKey con el modelo Cliente para representar el cliente que realizó el pedido
    customer = models.ForeignKey(Cliente, on_delete=models.RESTRICT)

    # Define un campo DateTimeField para almacenar la fecha de registro del pedido (se establecerá automáticamente)
    registration_date = models.DateTimeField(auto_now_add=True)

    # Define un campo CharField para almacenar el número de orden del pedido, 
    #order_number es llamado nro_pedido donde el profe
    order_number = models.CharField(max_length=20, null=True)

    # Define un campo DecimalField para almacenar el precio total del pedido, con un máximo de 10 dígitos y 2 decimales
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Define las opciones para el estado del pedido usando una tupla de tuplas (choices)
    STATUS_CHOICES = [
        ('0', 'Pending'),
        ('1', 'Paid'),
    ]

    # Define el campo para el estado del pedido y utiliza las opciones definidas anteriormente
    order_status = models.CharField(max_length=1, default='0', choices=STATUS_CHOICES)

    # Define el método __str__ para representar el objeto Pedido como una cadena
    #El método __str__ se utiliza para proporcionar una representación legible para humanos 
    def __str__(self):
        return f"Order number: {self.order_number}"



# Define el modelo PedidoDetalle para representar los detalles de un pedido
class PedidoDetalle(models.Model):

    # Define una relación ForeignKey con el modelo Pedido para representar el pedido al que pertenece este detalle
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT)

    # Define una relación ForeignKey con el modelo Producto para representar el producto que se incluye en este detalle
    product_name = models.ForeignKey(Producto, on_delete=models.RESTRICT)

    # Define un campo PositiveIntegerField para almacenar la cantidad de productos en este detalle
    quantity = models.PositiveIntegerField(default=1)

    # Almacena el costo que tuvo el producto en el momento de venderlo.
    # Es el precio del producto por la cantidad del mismo producto que se va a comprar
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # Añadí los argumentos max_digits y decimal_places

    # Define el método __str__ para representar el objeto PedidoDetalle como una cadena
    #El método __str__ se utiliza para proporcionar una representación legible para humanos 
    def __str__(self):
        # Retorna una cadena que incluye el nombre del producto y el nombre de usuario del cliente que hizo el pedido
        return f"Producto: {self.product_name.name} - Pedido de: {self.pedido.customer.usuario.username}"
