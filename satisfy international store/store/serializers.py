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
            errors['email'] = [
                {'field': 'email', 'message': 'Email must be provided'}]

        if password1 != attrs.get('password2'):
            errors['password'] = [
                {'field': 'password', 'message': 'Passwords must match'}]

        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                errors['password'] = [
                    {'field': 'password', 'message': list(e.messages)}]

        if CustomUser.objects.filter(email=email).exists():
            errors['email'] = [
                {'field': 'email', 'message': 'Email already taken.'}]

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

        if request:
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
            user = CustomUser.objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    return user
                raise serializers.ValidationError(
                    [{'field': 'password', 'message': 'Incorrect password'}])
            raise serializers.ValidationError(
                [{'field': 'email', 'message': 'Incorrect email'}])
        raise serializers.ValidationError(
            [{'fields': 'email and password', 'message': 'Email and password cannot be empty'}])
