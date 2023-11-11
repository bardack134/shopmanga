# Importamos la función 'render' desde el módulo 'shortcuts' de Django para renderizar las plantillas HTML.
from django.shortcuts import render, get_object_or_404, redirect
# Importamos los modelos 'Categoria' y 'Producto' desde el archivo '.models' de la aplicación actual.
from .models import Categoria, Producto

# Definimos una función llamada 'index' que será la vista para la página principal.
def index(request):

    # Obtenemos todos los objetos de la clase 'Producto' de la base de datos y los almacenamos en 'listaProductos'.
    listaProductos = Producto.objects.all()
    
    # Obtenemos todos los objetos de la clase 'Categoria' de la base de datos y los almacenamos en 'listacategorias'.
    listacategorias = Categoria.objects.all()

    # Creamos un diccionario 'context' que contiene datos que se pasarán a la plantilla HTML.
    context = {
        'productos': listaProductos,  # Pasamos la lista de productos.
        'categorias': listacategorias,  # Pasamos la lista de categorías.
    }

    # Renderizamos la plantilla 'index.html' con los datos del diccionario 'context' y la solicitud 'request'.
    return render(request, 'index.html', context)


#vista para filtrar productos por categoria
def ProductosPorCategoria(request, categoria_id):
    # Obtenemos la instancia de 'Categoria' con el ID proporcionado y la almacenamos en 'objCategoria'.
    objCategoria = Categoria.objects.get(id=categoria_id)

    
    # Obtenemos todos los productos relacionados con la categoría 'objCategoria' y los almacenamos en 'listaProductos'.
    listaProductos = objCategoria.producto_set.all()

    # Obtenemos todas las categorías de la base de datos y las almacenamos en 'listaCategoria'.
    listacategorias = Categoria.objects.all()

    # Creamos un diccionario 'context' que contiene datos que se pasarán a la plantilla HTML.
    context = {
        'categorias': listacategorias,  # Pasamos la lista de categorías.
        'productos': listaProductos,  # Pasamos la lista de productos relacionados con la categoría.
    }

    # Renderizamos la plantilla 'index.html' con los datos del diccionario 'context' y la solicitud 'request'.
    return render(request, 'index.html', context)


# Función para buscar un producto específico por medio de su nombre
def BuscarProducto(request):
    # La búsqueda se hace por medio de un formulario (la casilla buscar)
    # Capturamos la información que ha sido enviada por el método POST en este caso el formulario y le ponemos el nombre "name"
    name = request.POST['name'] 
    # Filtramos los objetos del modelo 'Producto' utilizando el método 'filter'.
    # Usamos '__icontains' para buscar objetos ignorando minusculas y matusculas
    # El resultado se almacena en 'listaProductos', que contendrá los productos que coinciden con el criterio de búsqueda.
    listaProductos = Producto.objects.filter(name__icontains=name)  

    listacategorias = Categoria.objects.all()

    # Creamos un diccionario 'context' que contiene datos que se pasarán a la plantilla HTML.
    context = {
        'categorias': listacategorias,  # Pasamos la lista de categorías.
        'productos': listaProductos,  # Pasamos la lista de productos relacionados con la categoría.
    }

    # Renderizamos la plantilla 'index.html' con los datos del diccionario 'context' y la solicitud 'request'.
    return render(request, 'index.html', context)



# Definición de la vista 'ProductoDetalle' que toma 'request' (solicitud HTTP) y 'producto_id' como parámetro.
def ProductoDetalle(request, producto_id):
    # Obtiene la instancia de 'Producto' con el ID proporcionado y la almacena en 'objProducto'.
    #objProducto = Producto.objects.get(id=producto_id)

    #get_object_or_404 se utiliza para manejo de errores, en el caso de que un producto no exista me mostrara error
    objProducto = get_object_or_404(Producto, pk=producto_id)
    # Crea un diccionario 'context' que contiene datos que se pasarán a la plantilla HTML.
    context = {
        'producto': objProducto  # Se pasa la instancia de producto a la plantilla con el nombre 'producto'.
    }

    # Renderiza la plantilla 'producto.html' con los datos del diccionario 'context' y la solicitud 'request'.
    return render(request, 'producto.html', context)


"""VISTAS PARA EL CARRITO DE COMPRAS"""
from .carrito import  Cart

#vista para mostrar el carrito de compras
def carrito(request):
    return render(request, 'carrito.html')


def agregarCarrito(request, producto_id):
    # Verifica si la solicitud HTTP es de tipo POST.
    if request.method == 'POST':

        # Si es POST, obtiene la cantidad del producto del formulario y la convierte a un entero.
        quantity = int(request.POST['quantity'])

    else:
        # Si no es POST (por ejemplo, una solicitud GET), establece la cantidad en 1 por defecto.
        quantity = 1

    
    # Obtener el objeto Producto correspondiente al producto_id proporcionado
    objProducto = Producto.objects.get(pk=producto_id)

    # Crear una instancia del carrito de compras (de la clase Cart del archivo carrito.py)
    carritoProducto = Cart(request)

    # Agregar el producto al carrito con la cantidad especificada
    carritoProducto.add(objProducto, quantity)

    # Verifica si la solicitud HTTP es de tipo GET.
    if request.method == 'GET':
        # Si es una solicitud GET, redirige al usuario a la página de inicio ('/').
        return redirect('/')



    # Renderizar la plantilla 'carrito.html' (aquí se supone que se mostrará el contenido del carrito)
    return render(request, 'carrito.html')



# Definimos la función "eliminarProductoCarrito" que se encargará de eliminar un producto del carrito de compras.
# Recibe el parámetro "request", que es el objeto que representa la solicitud HTTP recibida.
# También recibe el parámetro "producto_id", que es el ID del producto que se desea eliminar del carrito.
def eliminarProductoCarrito(request, producto_id):
    
        # Obtenemos el objeto "Producto" correspondiente al ID recibido como parámetro.
        producto = Producto.objects.get(pk=producto_id)

        # Creamos un objeto "carritoProducto" de la clase "Cart" y le pasamos el objeto "request" como parámetro.
        carritoProducto = Cart(request)

        # Llamamos al método "delete" del objeto "carritoProducto" y le pasamos el objeto "Producto" como parámetro.
        # Este método eliminará el producto del carrito de compras.
        carritoProducto.delete(producto)

        # Redireccionamos al usuario a la página del carrito después de eliminar el producto.
        return render(request, 'carrito.html')
    
"""except Producto.DoesNotExist:
        # Si el producto no existe,  manejamos el error adecuadamente aquí ( mostrando un mensaje al usuario).
        return render(request, 'error.html', {'mensaje': 'El producto no existe'})"""



def limpiarCarrito(request):
    # Creamos una instancia de la clase 'cart', pasando como parámetro el objeto 'request'.
    carritoProducto = Cart(request)

    # Utilizamos el método 'limpiar_carro()' de la clase 'carrito' para eliminar todos los productos del carrito.
    carritoProducto.clear()

    

    # Redirigimos al usuario a la página de la tienda después de limpiar el carrito.
    return render(request, 'carrito.html')