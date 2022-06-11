from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.hashers import make_password
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "password", "first_name", "last_name")

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def validate(self, data):
        user = get_user_model()(**data)
        password = data.get("password")
        errors = {}
        try:
            password_validation.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(data)


class UserSignInSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if not (email and password):
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")
        user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )
        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")
        data["user"] = user
        return data
