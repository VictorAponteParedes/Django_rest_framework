from django.contrib import admin
from profiles_api import models
# Register your models here.



# Con esto le estoy dando acseso al Administrador a que pueda editar los modelos en la pagina de administrador
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)