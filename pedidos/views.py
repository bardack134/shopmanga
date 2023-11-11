from django.shortcuts import redirect, render

#Los decoradores en Django, como @login_required, son funciones que modifican el comportamiento de otras funciones o métodos en Python
from django.contrib.auth.decorators import login_required

from autenticacion.forms import ClienteForm
from autenticacion.models import Cliente
from django.contrib.auth.models import User

from pedidos.models import Pedido, PedidoDetalle
from web.carrito import Cart
from web.models import Producto

from django.urls import reverse

from paypal.standard.forms import PayPalPaymentsForm
from django.core.mail import send_mail
# Create your views here.

@login_required
def registrarPedido(request):
    try:

        # Obtiene el cliente asociado al usuario actualmente autenticado o que inicio sesion
        clienteEditar = Cliente.objects.get(usuario=request.user)

        # Prepara los datos del cliente para prellenar el formulario
        datacliente = {
            'name': request.user.first_name,  # Nombre del usuario

            'Last_name': request.user.last_name,  # Apellido del usuario

            'email': request.user.email,  # Correo electrónico del usuario

            'address': clienteEditar.address,  # Dirección del cliente

            'phone_number': clienteEditar.phone_number,  # Número de teléfono del cliente

            'id_card': clienteEditar.id_card,  # Número de identificación del cliente

            'gender': clienteEditar.Gender,  # Género del cliente

            'birthdate': clienteEditar.birth_date,  # Fecha de nacimiento del cliente
        }

    #si el usuario no existe estrae solamente estos tres valores
    except:
        datacliente = {
            'name': request.user.first_name,  # Nombre del usuario

            'Last_name': request.user.last_name,  # Apellido del usuario

            'email': request.user.email, 
        }

    frmCliente=ClienteForm(datacliente)

    context={
        'frmCliente': frmCliente
    }

    return render(request, 'pedido.html', context)


@login_required
# Vista de confirmación de pedido
def confirmarPedido(request):

    context = {}

    if request.method == "POST":
        
        # Actualizamos datos del usuario, estos datos corresponden a la tabla usuario
        actUsuario = User.objects.get(pk=request.user.id)

        actUsuario.first_name = request.POST['name']

        actUsuario.last_name = request.POST['Last_name']
        """if 'last_name' in request.POST:
            last_name = request.POST['last_name']
        else:
            last_name = None  # o el valor por defecto que desees"""


        actUsuario.save()

        # Registramos o actualizamos cliente dependiento si  el cliente existe o no 
        try:
            
            #En esta linea de codigo se está tratando de obtener un objeto del modelo Cliente de la base de datos donde el campo usuario coincide con el usuario actualmente autenticado (request.user).
            clientePedido = Cliente.objects.get(usuario=request.user)
            clientePedido.phone_number = request.POST['phone_number']
            clientePedido.address = request.POST['address']
            clientePedido.save()

        # Si el cliente no existe, creamos un nuevo cliente
        except Cliente.DoesNotExist:
            clientePedido = Cliente()
            clientePedido.usuario = actUsuario
            clientePedido.address = request.POST['address']
            clientePedido.phone_number = request.POST['phone_number']
            clientePedido.save()

        # Registramos un nuevo pedido
        nroPedido = ''
        #el monto total esta almacenado en una variable de sesion llamada cartMontoTotal
        montoTotal = float(request.session.get('cartMontoTotal'))
        nuevoPedido = Pedido()
        nuevoPedido.customer = clientePedido
        nuevoPedido.save()

        #Registramos los detalles del pedido
        carritoPedido=request.session.get('cart')

        # Iteramos a través de los elementos del carrito de compras almacenados en la sesión del usuario
        for key, value in carritoPedido.items():

            # Obtenemos el producto correspondiente a partir de su ID almacenado en el carrito
            productoPedido = Producto.objects.get(pk=value['producto_id'])

            # Creamos una nueva instancia del modelo 'PedidoDetalle' para registrar los detalles del pedido
            detalle = PedidoDetalle()

            # Asignamos el pedido actual al detalle del pedido
            detalle.pedido = nuevoPedido

            # Al detalle del pedido asignamos el nombre del producto, este campo en nuestro modelo tiene una relacion ForeignKey con la tabla producto
            detalle.product_name = productoPedido

            # Asignamos la cantidad de productos del carrito al detalle del pedido
            detalle.cantidad = int(value['quantity'])

            # Asignamos el subtotal del producto al detalle del pedido
            detalle.subtotal = float(value['subtotal'])

            # Guardamos el detalle del pedido en la base de datos
            detalle.save()


        # Actualizar pedido
        #creamos un numero de pedido con la fecha de registro y pedido id con la palabra PED  de pedido
        #strftime('%Y')  convierta la fecha a una variable string
        nroPedido = 'PED' + nuevoPedido.registration_date.strftime('%Y') + str(nuevoPedido.id)
        nuevoPedido.order_number = nroPedido
        nuevoPedido.total_price = montoTotal
        nuevoPedido.save()

        #REGISTRAR VARIABLE DE SESSION PARA EL PEDIDO
           #Creamos nueva variable de session 
        request.session['pedidoId'] = nuevoPedido.id

        #CREAMOS BOTON DE PAYPAL
            # What you want the button to do.        
        paypal_dict = {
            "business": "sb-mtg9m27653910@business.example.com",
            "amount": montoTotal,
            "item_name": "CODIGO DEL PEDIDO: " + nroPedido,
            "invoice": nroPedido,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('pedido:gracias')),
            "cancel_return": request.build_absolute_uri(reverse('autenticacion:logoutUsuario')),
            "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
        }

        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        


        context={
            #nuevoPedido es una instancia de la clase pedido
            'pedido':nuevoPedido,
            "form": form,
        }


        #limpiamos el carrito de compras
        carrito=Cart(request)
        carrito.clear()

    # Renderizamos el template 'compra.html' como respuesta
    return render(request, 'compra.html', context)


#vista para mostrar gracias despues que el usuario ha hecho la compra
def gracias(request):
    #cuando retornamos al gracias despues de hacer la compra en nuestra url, se nos retorna una variable llmada PayerID
    #En el contexto de PayPal y otras pasarelas de pago, PayerID se refiere al identificador único del pagador (o comprador) durante una transacción. Es un identificador único asociado a la cuenta o método de pago del usuario que realizó la compra. Cuando un usuario completa un proceso de pago en PayPal y es redirigido de vuelta a tu sitio web, el PayerID se utiliza para identificar de manera única al comprador y asociar la transacción a su cuenta de PayPal. Este identificador puede ser utilizado para realizar operaciones posteriores, como reembolsos o consultas de estado de pago.
    paypalId = request.GET.get('PayerID', None)#PayerID Es el nombre de la variable, si no la encuentra le ponemos None

    if paypalId is not None:

        #pedidoId es una variable de sesionn y con la sgt line ade codigo obtenemos su valor 
        pedidoId = request.session.get('pedidoId')

        #obtenemos el pedido asignado a la variable id
        pedido = Pedido.objects.get(pk=pedidoId)

        #1 significa pagado, lo asignamos en nuestro modelo pedido
        pedido.order_status = '1'

        #guardamos cambius
        pedido.save()

        #enviamos correo de confirmacion al usuario con los detalles de su pedido
        send_mail(
            #subject del mail
            'THANK YOU FOR YOUR PURCHASE',

            #Our message
            'your order number is ' + pedido.order_number,

            #donde enviamos nuestro mail
            'ricardoantoniogomezvillalobos@gmail.com',

            #correo del usuario o lista de correos
            [request.user.email ],

            fail_silently=False,

            
        )
        #print(pedido.order_number)  prueba si se envia el order number correctamente
        context = {
            #en nuestra pagina de gracias queremos poner la informacion del pedido e informar al usuario que le enviaremos un correo con la info del pedidu
            'pedido':pedido
        }
    else:
        return redirect('/')

    return render(request, 'gracias.html', context)






"""PRUEBA DE LA LIBRERIA PAYPAL"""


def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": "sb-mtg9m27653910@business.example.com",
        "amount": "10.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('web:index')),
        "cancel_return": request.build_absolute_uri(reverse('autenticacion:logoutUsuario')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)