from rest_framework import serializers


class UserameNotMeMixin:
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f"Имя пользователя не должно быть '{value}'"
            )
        return value
