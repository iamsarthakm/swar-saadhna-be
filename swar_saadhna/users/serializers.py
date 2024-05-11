from rest_framework import serializers


class UserRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=10, allow_null=True, required=False)
    email = serializers.EmailField(max_length=255, allow_null=True, required=False)

    def validate(self, attrs):
        return super().validate(attrs)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        return super().validate(attrs)
