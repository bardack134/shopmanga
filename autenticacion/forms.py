from django import forms
"""CREAMOS ARCHIVO FORMS.PY Y USAMOS LA CLASE forms.Form de django para la creacion de formularios"""

#clase dateinput para personalizar el dateinput, usamos esta clase en el campo birthday de la clase ClienteForm
class DateInput(forms.DateInput):
    input_type='date'

#forms.Form es una clase base en Django que se utiliza para crear formularios web. Representa un formulario HTML y se utiliza para definir campos y validaciones en el formulario.
class ClienteForm(forms.Form):
    #campos que necesitamos en nuestro formulario

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    id_card=forms.CharField(label='Identification Number', required=True, max_length=100)

    name=forms.CharField(label='Name', required=True, max_length=200)

    Last_name=forms.CharField(label='Surname', required=True, max_length=200)
    
    email=forms.EmailField(label='Email', required=True, max_length=50)
    
    #widget=forms.Textarea es útil para personalizar la representación de un campo de texto en un formulario, permitiendo que los usuarios ingresen texto largo de manera más cómoda.
    address=forms.CharField(label='Address', required=True, widget=forms.Textarea)
    
    phone_number=forms.CharField(label='Phone number', required=True, max_length=20)

    gender=forms.ChoiceField(label='Gender', choices=GENDER_CHOICES)
    
    birthdate= forms.DateField(label='Birthdate', input_formats=['%Y-%m-%d'], widget=DateInput())
    

    """INTENTAR HACER DESPUES UN SISTMA DE VALIDACION PARA COMPROBAR SI YA EXISTE EL USUARIO EN LA BASE DE DATOS"""