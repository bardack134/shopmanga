from django.urls import path, include

from . import views

#de las vistas importamos las clases que creamos
#from .views import pedido_en_proceso

app_name='pedido'


urlpatterns = [
        
    
    path('registrarPedido', views.registrarPedido, name='registrarPedido'),
    
    path('pruebapaypal/', views.view_that_asks_for_money, name='pruebapaypal'),
   
    path('confirmarPedido/', views.confirmarPedido, name='confirmarPedido'),

    path('gracias/', views.gracias, name='gracias'),
    #path('pedido_procesado/', views.pedido_en_proceso.as_view(), name='pedido_procesado'),  # Cambia la ruta para el pedido procesado

]