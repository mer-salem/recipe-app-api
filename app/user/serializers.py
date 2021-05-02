from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from core.models import User
from core.models import Me


class SerializerUser(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5, 'style': {'input_type': 'password'}},
                        }

        # def create(self, validate_data):
        #     user = get_user_model().objects.create_user(**validate_data)
        #     return user

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    # name = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(self.context.get('request'),
                            username=email, password=password)
        if not user:
            msg = ('unable to authenticate with provide credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
