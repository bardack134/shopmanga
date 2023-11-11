from django.urls import path



from autenticacion import views

app_name='autenticacion'

urlpatterns = [
    
    path('crearUsuario', views.crearUsuario, name='crearUsuario'),

    path('cuenta', views.cuentaUsuario, name='cuentaUsuario'),

    path('actualizarCliente', views.actualizarCliente, name='actualizarCliente'),

    path('loginUsuario', views.loginUsuario, name='loginUsuario'),
    
    path('logout', views.logoutUsuario, name='logoutUsuario'),

    # Asignamos la función 'cerrar_sesion' a la URL 'cerrar/', con el nombre 'cerrar_sesion'.
    #path('cerrar/', cerrar_sesion, name='cerrar_sesion'),

    

#    path('login/', LoginView.as_view(), name='login'),
]
