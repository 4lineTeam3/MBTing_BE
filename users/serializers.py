from .models import User,Spec
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user
    

class ImageUrlField(serializers.ImageField):
    def to_representation(self, value):
        if value:
            return value.url
        return None

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_picture = ImageUrlField()

    class Meta:
        model = User
        fields = '__all__'
        depth =1

class SpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spec
        fields = ('spec',)

