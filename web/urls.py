

from django.urls import path

from . import views


app_name='web'
# Define las URL de tu aplicación
urlpatterns = [
    #dejo la raiz vacia para definir que ese sera su pagina home
    path('', views.index, name='index'),
    path('ProductosPorCategoria/<int:categoria_id>', views.ProductosPorCategoria, name='ProductosPorCategoria'),
    path('BuscarProducto', views.BuscarProducto, name='BuscarProducto'),
    path('Producto/<int:producto_id>', views.ProductoDetalle, name='ProductoDetalle'),
    path('carrito', views.carrito, name='carrito'),
    path('agregarCarrito/<int:producto_id>', views.agregarCarrito, name='agregarCarrito'),
    path('eliminarProductoCarrito/<int:producto_id>', views.eliminarProductoCarrito, name='eliminarProductoCarrito'),
    path('limpiarCarrito', views.limpiarCarrito, name='limpiarCarrito'),
]




