from django.shortcuts import redirect, render

from django.contrib.auth.models import User

from django.contrib.auth import login,logout,authenticate

from django.contrib.auth.decorators import login_required

from .models import Cliente

from web.models import Categoria, Producto

#importamos el formulario hecho en el archivo form.py
from .forms import ClienteForm
from django.urls import reverse
# Create your views here.


"""VISTAS PARA CLIENTES Y USUARIOS"""

# función llamada 'crearUsuario' corresponde al registro de usuario para crear cuenta
def crearUsuario(request):

    # Comprueba si la solicitud es de tipo POST (generalmente se utiliza para enviar datos).
    if request.method == 'POST':

        # se obtienen los datos del formulario con nombre 'nuevoUsuario' y 'nuevoPassword' del objeto 'request.POST'.
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']


        # Crea un nuevo usuario en la base de datos user utilizando los datos proporcionados.
        # Esto crea un usuario con el nombre de usuario 'dataUsuario' y la contraseña 'dataPassword'.
        nuevoUsuario = User.objects.create_user(username=dataUsuario, password=dataPassword)

        # se comprueba  se ha creado correctamente un nuevo usuario.
        # si nuevoUsuario es no vacio
        if nuevoUsuario is not None:

            # Si se creó correctamente, inicia sesión automáticamente al nuevo usuario.
            login(request, nuevoUsuario)

            return redirect('autenticacion:cuentaUsuario')
            # Otra forma de hacerlo es escribir directamente la url return redirect('/cuentaUsuario')
        

    # se renderiza la plantilla 'login.html' y se devuelve como respuesta.
    # Esta línea se ejecutará tanto si se procesa el formulario como si no. es decir si no es metodo post, simplemente se va a mostrar el formulario en pantalla
    return render(request, 'login.html')


# vista para crear el formulario de registro de cliente ClienteForm,Obtiene el cliente asociado al usuario actualmente autenticado o que inicio sesion
@login_required
def cuentaUsuario(request):
    #intentamos ejecutar esta parte, si el usuario no existe me mostrara error y ejecutara el except
    try:

        # Obtiene el cliente asociado al usuario actualmente autenticado o que inicio sesion
        clienteEditar = Cliente.objects.get(usuario=request.user)

        # Prepara los datos del cliente para prellenar el formulario que hicimos en form.py
        datacliente = {
            #los tres primeros datos vienen de la tabla user
            'name': request.user.first_name,  # Nombre del usuario

            'Last_name': request.user.last_name,  # Apellido del usuario

            'email': request.user.email,  # Correo electrónico del usuario

            #apartir de aca los datos vienen de la tabla cliente
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

    # Crea una instancia del formulario 'ClienteForm' utilizando los datos prellenados
    frmCliente = ClienteForm(datacliente)

    # Crea un contexto que contiene el formulario 'frmCliente'
    context = {
        'frmCliente': frmCliente
    }

    # Renderiza la plantilla 'cuenta.html' con el contexto proporcionado
    return render(request, 'cuenta.html', context)


# Función para iniciar sesión de un usuario
def loginUsuario(request):

    #cuando intentamos entrar en nuestra tienda a la sesion make an order, nos hace la validacion si estamos autenticados o no, al hacer el login de usuario, en nuestra urls hay una variable que se llama next, esta variable indica la url a la que se debe ir despues de hacer el login, trabajaremos con esa variable next, que se pasa en el metodo get

    #GET es el metodo principal y dentro esta el metodo get, recibe como parametro la variable next, y si no viene ninguna sera 'None'
    paginaDestino = request.GET.get('next', None)

    context = {
        'destino':paginaDestino
    }  # Inicializa un diccionario de contexto

    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST (se envían datos)

        # Obtiene los datos del formulario de inicio de sesión ('usuario' y 'password') del objeto 'request.POST'
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']

        # usamos el metodo autenticate para autenticar el usuario
        usuarioAuth = authenticate(request, username=dataUsuario, password=dataPassword)

        if usuarioAuth is not None:  # Si la autenticación es exitosa (el usuario existe y la contraseña es correcta)

            login(request, usuarioAuth)  # Inicia sesión con el usuario autenticado

            # Redirige a la página de cuenta del usuario
            
            if dataDestino != 'None':
                return redirect(dataDestino)

            return redirect(reverse('autenticacion:cuentaUsuario'))


        else:
            context = {
                'mensajeError': 'Invalid username or password'  # Configura un mensaje de error si la autenticación falla
            }

    # Renderiza la plantilla 'login.html' con el contexto proporcionado
    return render(request, 'login.html', context)


#funcion para cerrar sesion
def logoutUsuario(request):
    # Utilizamos la función logout() para cerrar la sesión del usuario.
    logout(request)

    # Redirigimos al usuario al login
    return render(request, 'login.html')



def actualizarCliente(request):
    # Define una variable 'mensaje' para almacenar un mensaje, inicialmente vacío
    mensaje = ""
    
    # Obtiene el usuario actual
    user = request.user

    # Comprueba si el método de solicitud HTTP es POST, viene con los datos ingresados por el usuario
    if request.method == 'POST':

        # Crea un formulario 'frmCliente' y lo rellena con los datos POST
        frmCliente = ClienteForm(request.POST)

        # Comprueba si el formulario es válido
        if frmCliente.is_valid():

            # Extrae los datos limpios del formulario y almacenados en cleaned_data
            dataCliente = frmCliente.cleaned_data

            # Verifica si el cliente ya existe en la base de datos
            cliente_existente = Cliente.objects.filter(usuario=user).first()

            if cliente_existente:

                # Si el cliente existe, actualiza sus datos
                cliente_existente.id_card = dataCliente["id_card"]
                cliente_existente.address = dataCliente["address"]
                cliente_existente.phone_number = dataCliente["phone_number"]
                cliente_existente.Gender = dataCliente["gender"]
                cliente_existente.birth_date = dataCliente["birthdate"]

                # Guarda los cambios en el cliente existente
                cliente_existente.save()

                # Obtiene el usuario actual para actualizar su información
                actUsuario = User.objects.get(pk=user.id)

                # Actualiza el nombre, apellido y correo electrónico del usuario
                actUsuario.first_name = dataCliente["name"]
                actUsuario.last_name = dataCliente["Last_name"]
                actUsuario.email = dataCliente["email"]

                # Guarda la información del usuario actualizada
                actUsuario.save()

                # Establece el mensaje de éxito
                mensaje = "User's Information updated"
            else:
                # Si el cliente no existe, crea uno nuevo
                nuevoCliente = Cliente()

                # Asocia el 'Cliente' con el usuario actual
                nuevoCliente.usuario = user

                # Rellena los campos del modelo 'Cliente' con los datos del formulario
                nuevoCliente.id_card = dataCliente["id_card"]
                nuevoCliente.address = dataCliente["address"]
                nuevoCliente.phone_number = dataCliente["phone_number"]
                nuevoCliente.Gender = dataCliente["gender"]
                nuevoCliente.birth_date = dataCliente["birthdate"]

                # Guarda la nueva instancia de 'Cliente'
                nuevoCliente.save()

                # Obtiene el usuario actual para actualizar su información
                actUsuario = User.objects.get(pk=user.id)

                # Actualiza el nombre, apellido y correo electrónico del usuario con los datos del formulario
                actUsuario.first_name = dataCliente["name"]
                actUsuario.last_name = dataCliente["Last_name"]
                actUsuario.email = dataCliente["email"]

                # Guarda la información del usuario actualizada
                actUsuario.save()

                # Establece el mensaje de éxito
                mensaje = "New user's Information created"

    context = {
        'mensaje': mensaje,
        'frmCliente': frmCliente
    }
    
    # Renderiza la plantilla 'cuenta.html' con un mensaje opcional
    return render(request, 'cuenta.html', context)


"""Ambas vistas permiten la actualización de datos, pero la primera vista (actualizarCliente(request)) se enfoca más en la manipulación de datos del formulario y su procesamiento directo, mientras que la segunda vista (cuentaUsuario(request)) se enfoca en obtener datos preexistentes del cliente (si existen) para mostrarlos en el formulario. Ambas vistas siguen una estructura diferente para lograr el mismo objetivo de permitir a los usuarios actualizar sus datos"""