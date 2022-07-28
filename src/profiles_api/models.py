from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import (
    settings,
)  # Con esto voy a obtener algunos settings de settings.py del proyecto


class UserProfileManager(BaseUserManager):
    """Manager para perfiles de usuario"""

    def create_user(
        selt, name, email, password=None
    ):  # Le estoy pasando los parametros que los Usuarios tendran para el registro
        """Crear nuevo User Profile"""
        if not email:
            # Con esto le digo que tendra un error caso el usuario no tenga un Email
            raise ValueError("Usuario debe tener un Email")

        # Con esto le estoy diciendo que de mayusculas pasen a minusculas
        email = selt.normalize_email(email)
        # Con esto estoy definiendo mi Objeto de Usuario
        user = selt.model(email=email, name=name)

        user.set_password(password)
        # Con esto lo que estoy haciendo es poder guardar mi usuario nuevo
        user.save(using=selt._db)

        return user

        # Super Usuario o Abministradores

    def create_superuser(selt, email, name, password):
        # Aqui estoy reutilizando mi codigo o funcion de crear un usuario
        user = selt.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=selt._db)
        return user


# Create your models here.


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Modelos de Base de Datos para Usuarios en el Sist ema"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        """Obtener el Nombre Completo de Usuario"""
        return self.name

    def get_short_name(selt):
        """Obtener el Nombre Completo de Usuario"""
        return selt.name

    def __str__(self):
        return self.email


class ProfileFeedItem(models.Model):
    """Perfil status Update"""

    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Con esto le digo que si el usuario se borra tambien todo su historial se tiene que borrar para asi poder enlistar lo que 
    )

    # Este es el texto que mostramos cuando hagamos el Update
    status_text = models.CharField(max_length=225)
    create_on = models.DateTimeField(
        auto_now_add=True
    )  # Con esto le estoy diciendo cuando fue creado

    def __str__(self):
        """Retornar el modelo como cadena"""
        return self.status_text
