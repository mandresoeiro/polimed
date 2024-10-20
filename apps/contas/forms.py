from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from contas.models import MyUser

#TODO Quando for customizar o formulario pode colocar "custom", no campo. Ex. CustomUserCreationForm
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmação de Senha", widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        #TODO Renomeando as labels
        labels = {
            'email': 'Email',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'is_active': 'Usúario Ativo?'
        }

    def __init__(self, *args, **kwargs):#TODO No momento que executar o formulario sera feito um for 
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'#TODO Adiciona a classe bootstrap
            else:
                field.widget.attrs['class'] = 'form-control'

    #TODO Da documentação do django, para fazer o clean de password2, p quando n fizer math.
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Senha não estão iguais!")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format (O format hashed no Django é um conjunto de elementos 
        # que inclui o hastype, salt e hash, separados por um caracter dolar ('$'). )
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):#TODO Cria um formulario para alterar o usuario
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'is_active']
        # help_texts = {'username': None}#TODO Remove o campo de username(MENSAGENS DE AJUDA)
        labels = {#TODO Renomeando as labels
            'email': 'Email',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'is_active': 'Usúario Ativo?'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():#TODO Pegando os campos do formulario
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
