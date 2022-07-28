from dataclasses import fields
from rest_framework import serializers
from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializa un campo para provar nuestro APIView"""

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializa objeto de perfil de usuario"""

    class Meta:
        model = models.UserProfile
        fields = ("id", "email", "name", "password")
        extra_kwargs = {
            "password": {
                "write_only": True,  # Esto hace que la clave se vea solamente cuando estamos creando
                "style": {
                    "input_type": "password"
                },  # Con esto estoy haciendo que cuando el usuario escriba su clave solo muestren los asteriscos
            }
        }

    def create(self, validated_data):

        """Creacion y Retornando Nuevo Usuario"""

        user = models.UserProfile.objects.create_user(
            # Aca lo que estoy haciendo es poder validar los campos
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
        )
        return user

    def update(selt, instance, validated_data):
        """Actualiza cuenta del Usuario"""
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """ Serializador de profile feed items """
    class Meta:
        model = models.ProfileFeedItem
        fields = ("id" , "user_profile" , "status_text", "create_on")
        extra_kwargs = {"user_profile":{"read_only": True}}