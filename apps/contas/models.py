from django.db import models

# TODO Modelo customizados de usuario
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MyUserManager(BaseUserManager):#TODO Gerenciador de usuários
    def create_user(self, email, password=None, **kwargs):#TODO Cria um novo usuario
        if not email:#TODO Verifica se o email esta vazio
            raise ValueError('Users must have an email address')#TODO Todos usuários devem ter um endereço de e-mail
        user = self.model(email=self.normalize_email(email), **kwargs) #TODO email normalizado
        user.set_password(password)#TODO Senha criptografada
        user.save()#TODO Salva o novo usuario
        return user #TODO Retorna o novo usuario

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)#TODO Permissão de administrador
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # TODO saber se ususario esta ativo
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        'date joined', auto_now_add=True)  # TODO data de cadastro

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
