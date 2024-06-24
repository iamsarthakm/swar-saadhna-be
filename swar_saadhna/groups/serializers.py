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


class GetGroupAudiosSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    limit = serializers.IntegerField(default=0)
    offset = serializers.IntegerField(default=10)
    search = serializers.CharField(max_length=255, default="")

    def validate(self, attrs):
        return super().validate(attrs)


class GetGroupUsersSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    limit = serializers.IntegerField(default=0)
    offset = serializers.IntegerField(default=10)
    search = serializers.CharField(max_length=255, default="")

    def validate(self, attrs):
        return super().validate(attrs)


class AddGroupAudiosSerializer(serializers.Serializer):
    audio_ids = serializers.ListField(child=serializers.IntegerField())
    group_id = serializers.IntegerField()

    def validate(self, attrs):
        return super().validate(attrs)


class AddGroupUsersSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())
    group_id = serializers.IntegerField()

    def validate(self, attrs):
        return super().validate(attrs)


class CreateGroupCodeSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()

    def validate(self, attrs):
        return super().validate(attrs)


class JoinGroupSerializer(serializers.Serializer):
    # group_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        return super().validate(attrs)
