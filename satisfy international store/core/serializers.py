from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


CustomUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    password2 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'password2']

    def validate(self, attrs):
        password1 = attrs.get('password')
        email = attrs.get('email')

        errors = {}

        if not email:
            errors['email'] = ['Email must be provided']

        if password1 != attrs.get('password2'):
            errors['password'] = ['Passwords must match']

        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                errors['password'] = [ list(e.messages)]

        if CustomUser.objects.filter(email=email).exists():
            errors['email'] = ['Email already taken.']

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        represenation = super().to_representation(instance)
        request = self.context.get('request')

        
        if request.method == 'PATCH':
            represenation.pop('id', None)
        represenation.pop('password', None)
        represenation.pop('password2', None)

        return represenation


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get(
                'request'), username=email, password=password)
            if user:
                return user
            else:
                raise serializers.ValidationError('Invalid email or password')
        raise serializers.ValidationError(
            'Must include both "email" and "password"')


class LogoutUserSerializer(serializers.Serializer):
    """This is specified because of the drf swagger documentation"""
    refresh = serializers.CharField()
