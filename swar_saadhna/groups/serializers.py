from rest_framework import serializers


class AddGroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)

    def validate(self, attrs):
        return super().validate(attrs)


class GetGroupSerializer(serializers.Serializer):
    search = serializers.CharField(max_length=255, default="")
    limit = serializers.IntegerField(default=0)
    offset = serializers.IntegerField(default=10)

    def validate(self, attrs):
        return super().validate(attrs)
