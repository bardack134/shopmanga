class Cart:
    #constructor de la clase,  Se ejecuta automáticamente cuando se crea un nuevo objeto de la clase "carrito".
    def __init__(self, request):
        #atributos del constructor, request, session,  carro

        #En esta línea, se asigna el valor del parámetro "request" que se recibió en el constructor al atributo "request" del objeto "carro".
        self.request=request

        #Aquí, se asigna el atributo "session" del objeto "request" al atributo "session" del objeto "carro". El atributo "session" es un objeto que representa la sesión actual de Django y se utiliza para almacenar información entre solicitudes HTTP.
        self.session=request.session

        #.get('carro'): get() es un método que se puede utilizar en diccionarios (y en este caso, el objeto de sesión se comporta como un diccionario). Recibe un argumento que es la clave que queremos buscar en el diccionario y devuelve el valor asociado con esa clave. Si la clave no existe en el diccionario, en lugar de arrojar un error, retorna None o un valor predeterminado que se puede proporcionar como segundo argumento de get() (en este caso no se proporciona, por lo que si no encuentra la clave, el valor será None).

        #(Se verifica si existe el carrito de compras)
        cart=self.session.get('cart')

        #variable para saber el monto total de dinero a pagar, miramos si eexiste esta variable de sesion
        montoTotal = self.session.get('cartMontoTotal')

        #si la clave no existe en el diccionario creamos un diccionario asociado a esa clave
        #(si no existe el carrito de compras, se crea)
        if not cart:

        #se está asignando un nuevo diccionario vacío a dos variables al mismo tiempo: carro y self.session['carro'].
        # 
        # Esta linea crea un nuevo diccionario vacío {} y lo asigna a la clave 'carro' dentro del objeto de sesión (self.session).
        # (creamos el carrito de compras)  
            cart=self.session['cart']={}

            #si no existe la variable de session llamada cartMontoTotal la creamos
            montoTotal=self.session['cartMontoTotal']='0'
        
        

        #Con esta linea de codigo siempre se crea el carro independiente de todo lo detras
        #(lo pasamos como un atributo del constructor)
        self.cart=cart

        self.montoTotal=float(montoTotal)
    
    # Función para agregar productos al carro, recibe 2 parámetros: self y el producto que queremos agregar al carro
    def add(self, producto, quantity):

        # Comprobamos si el producto ya está en el carro a través de su ID.
        if str(producto.id) not in self.cart.keys():

            # Si el ID del producto no está en el diccionario self.cart, significa que el producto no ha    sido agregado previamente al carro.
            # En ese caso, añadimos el producto al carro como un nuevo diccionario con la siguiente     información:
            self.cart[producto.id] = {
                "producto_id": producto.id,
                "name": producto.name,
                "quantity": quantity,
                "price": str(producto.price),
                "image": producto.image.url,
                "category": producto.category.name,
                "subtotal": str(quantity * producto.price),  # Calculamos el subtotal
            }
        else:
            # Si el producto ya se encuentra en el carro, es decir, el ID del producto ya está presente en  las claves del diccionario self.cart, actualizamos la información del producto.
            for key, value in self.cart.items():

                # Por cada iteración del bucle, verificamos si la clave del diccionario (key) coincide con  el ID del producto que queremos agregar (str(producto.id)).
                if key == str(producto.id):

                    # Incrementamos la cantidad del producto, ya que el producto ya existe en el carro.
                    # Esto se hace actualizando el valor correspondiente en el diccionario self.cart. La    cantidad del producto se encuentra dentro del diccionario interno bajo la clave    "quantity".
                    value["quantity"] = str(int(value["quantity"]) + quantity)

                    # Calculamos el nuevo subtotal con la cantidad actualizada y el precio del producto.
                    value["subtotal"] = str(float(value["quantity"]) * float(value["price"]))

                    # Rompemos el bucle, ya que hemos encontrado el producto en el carro y ya hemos     actualizado la cantidad.
                    break

        # Llamamos al método save() para guardar los cambios en la sesión.
        self.save()



    # guarda cambios en el carrito de compras
    def save(self):

        # Inicializamos la variable montTotal para rastrear el monto total del carrito.
        montoTotal = 0

        # Iteramos a través de los elementos en el carrito, donde 'key' es el identificador del producto y 'value' es un diccionario con detalles del producto.
        for key, value in self.cart.items():

            # Sumamos el subtotal del producto actual al monto total.
            montoTotal += float(value["subtotal"])

        # Guardamos el monto total en la variable de session para su posterior uso.
        self.session['cartMontoTotal'] = montoTotal


        # Guardamos el diccionario self.carro en la sesión con la clave 'carro'
        #Esto asegura que los datos del carro se conserven entre las solicitudes HTTP y estén disponibles para el usuario en futuras interacciones con la aplicación.
        self.session['cart'] = self.cart

        # Indicamos que la sesión ha sido modificada, para asegurarnos de que los cambios se guarden correctamente

        #Esta configuración es necesaria para que Django sepa que se han realizado cambios en la sesión y que estos cambios deben ser guardados en el almacenamiento persistente (por ejemplo, en una base de datos o en la memoria del servidor) al finalizar la solicitud HTTP. Si no establecemos self.session.modified = 0True, los cambios en la sesión podrían no guardarse correctamente.
        self.session.modified = True


    # Esta función se encarga de eliminar un producto específico del carro de compras.
    def delete(self, producto):

        producto_id=str(producto.id)

        # verifica si el id del producto que queremos eliminar está presente como una clave en el diccionario self.cart. Si es así, significa que el producto está en el carro y podemos proceder a eliminarlo.
        if  producto_id in self.cart:

            # Si el producto está en el carro, lo eliminamos usando la función `del`
            #Usamos str(producto.id) como clave para acceder al elemento específico en el diccionario y eliminarlo.
            del self.cart[producto_id]

            # Guardamos los cambios en la sesión después de eliminar el producto
            #Esto asegura que los cambios en el carro se conserven y estén disponibles en futuras interacciones del usuario con la aplicación.
            self.save()

    def restar_producto(self, producto):
            
        # Un bucle que recorre todas las clave, valor del diccionario self.carro
            for key, value in self.carro.items():

                #Por cada iteración del bucle, se verifica si la clave del diccionario (key) coincide con el ID del producto que queremos agregar (str(producto.id)).
                if key == str(producto.id):

                    # disminuimos la cantidad del producto en 1, ya que el producto ya existe en el carro.
                    #Esto se hace actualizando el valor correspondiente en el diccionario self.carro. La cantidad del producto se encuentra dentro del diccionario interno bajo la clave "cantidad".
                    value["cantidad"] = value["cantidad"] - 1

                    # Resta el precio actual del producto almacenado en el diccionario "value" con el precio del producto llamado "producto" y actualiza el campo "precio" en el diccionario "value".
                    value["precio"] = float(value["precio"]) - producto.precio

                    if value["cantidad"]<1:

                        self.eliminar(producto)
                     

                    # Rompemos el bucle, ya que hemos encontrado el producto en el carro y ya hemos actualizado la cantidad
                    break

            # Guardamos los cambios en la sesión después de eliminar el producto
            #Esto asegura que los cambios en el carro se conserven y estén disponibles en futuras interacciones del usuario con la aplicación.
            self.guardar_carro()


    # Con esta función buscamos eliminar todos los productos que se encuentren en el carro de compras
    def clear(self):
        # Vaciamos el diccionario `self.cart` asignándole un diccionario vacío
        self.session['cart'] = {}
        
        self.session['cartMontoTotal'] = "0"
    
        # Esta configuración es necesaria para que Django sepa que se han realizado cambios en la sesión y que estos    cambios deben ser guardados en el almacenamiento persistente (por ejemplo, en una base de datos o en la memoria    del servidor) al finalizar la solicitud HTTP. Si no establecemos `self.session.modified = True`, los cambios en    la sesión podrían no guardarse correctamente.
        self.session.modified = True







    






