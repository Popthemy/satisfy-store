from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)
    password = serializers.CharField(max_length=255,write_only=True)
    password2 = serializers.CharField(max_length=255,write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password','password2']

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
