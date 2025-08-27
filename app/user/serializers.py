"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

# SERIALIZER IS  A WAY TO CONVERT "OBJECT"
# INTO "PYTHON OBJECT"
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {"password": {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    # THE DATA W/C IS PASSED THROUGH VALIDATION SERIALIZER: "validated_data"
    def update(self, instance, validated_data):
        """Update and return user."""
        # BY DEFAULT THE PWD IS NOT CHANGED
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        # IF THE PWD IS SPECIFIED BY USER:
        if password:
            user.set_password(password)
            user.save()  # SAVE THE NEW PWD

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        # the email coming from input
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
