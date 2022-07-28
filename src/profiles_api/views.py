from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    status,
    filters,
)  # El filter me siver para poder filtrar los usuarios que deseo buscar tanto por nombre ,  email y por ID
from profiles_api import serializers, models, permissions
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated # Con esto le estoy diciendo que solo los usuarios autenticados puedan leer el API 

# Create your views here.


class HelloApiView(APIView):
    """API View de Prueba"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Retornar lista de caracteristicas del api view"""
        an_apiview = [
            "Usamos metodos HTTP como funcinones (get , post , patch , put , delete)",
            "Es similar a una vista tradicional de Django",
            "No da mayor control sobre la logica de nuestra aplicacion",
            "Esta mapeando manualmente a los URLs",
        ]

        # Estoy respondiendo en formato json
        return Response({"message": "Hello", "an_apiview": an_apiview})

    def post(self, request):
        """Crea un mensaje con nuestro nombre"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"
            return Response({"message": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Maneja actualizar un Objeto"""
        return Response({"method": "PUT"})

        """ Maneja actualizaciones de un objeto parcialmente """
        return Response({"method": "PATCH"})

    def delete(self, request, pk=None):
        """Borra un Objeto"""
        return Response({"method": "DELETE"})


########################### LOS VIEWSET ########################################


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Retornar Mensaje de Hola Mundo"""
        a_viewset = [
            "Usa acciones (list , create , retrieve , update , partial_update)",
            "Automaticamente mapea a los URLs usando Routers",
            "Provee mas funcionalidad con menos codigo",
        ]

        return Response({"message": "Hola!", "a_viewset": a_viewset})

    def create(self, request):
        """Retornar Mensaje de Hola Mundo"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hola {name}"
            return Response({"message": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Obtiene un Objeto y su ID"""
        return Response({"http_method": "GET"})

    def update(self, request, pk=None):
        """Actualiza un Objeto"""
        return Response({"method": "PUT"})

    def partial_update(self, request, pk=None):
        """Actualiza parcialmente ahora un Objeto"""
        return Response({"method": "PATCH"})

    def destroy(self, request, pk=None):
        """Creacion y Retornando Nuevo Usuario"""
        return Response({"method": "DELETE"})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Crear y Actualizar Perfiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = (
        models.UserProfile.objects.all()
    )  # aqui estoy obteniendo todos los objetos que han sifo creado
    authentication_classes = (
        TokenAuthentication,
    )  # Esto sirve para que es el usuario se autentique
    permission_classes = (
        permissions.UpdateOwnProfile,
    )  # Con esto el usuario tiene permiso de hacer ciertas acciones en nuestra app
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        "name",
        "email",
    )


class UserLoginApiView(ObtainAuthToken):
    """Crear tokens de autenticacion de usuario"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Maneja el Crear ,Leer y actualizar el Profile Feed"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnProfile, IsAuthenticated)

    def perfom_create(self, serializer):
        """Setear el perfil de usuario para el usuario que esta logeado"""
        serializer.save(user_profile=self.request.user)
