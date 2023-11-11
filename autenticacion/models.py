from django.db import models
from django.contrib.auth.models import User

"""MODELO PARA TRABAJAR CON LOS USUARIOS DE NUESTRA PAGINA"""

# Define la clase  Cliente que se relaciona con el modelo User de Django.
class Cliente(models.Model):
    # Relación uno a uno con el modelo User de Django.
    usuario = models.OneToOneField(User, on_delete=models.RESTRICT)

    # El campo "id_card" representa la cédula o número de identificación.
    id_card = models.CharField(max_length=10)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    # El campo "Gender" representa el género con una longitud máxima de 1 caracter y un valor predeterminado de 'M' (Masculino).
    Gender = models.CharField(max_length=1, default='M', choices=GENDER_CHOICES)

    # El campo "phone_number" representa el número de teléfono con una longitud máxima de 20 caracteres.
    phone_number = models.CharField(max_length=20)

    # El campo "birth_date" representa la fecha de nacimiento como una fecha (DateField) y puede ser nulo (null=True).
    birth_date = models.DateField(null=True)

    # El campo "address" representa la dirección como un campo de texto largo.
    address = models.TextField()

    # El método "__str__" define cómo se mostrará el objeto Cliente como una cadena.
    def __str__(self):
        # Devuelve el nombre de usuario  relacionado con el modelo users.
        return self.usuario.username
