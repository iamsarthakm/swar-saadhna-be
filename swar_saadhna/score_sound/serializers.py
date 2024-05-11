from rest_framework import serializers
from .models import AudioScore


class CreateAudiosSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    scale = serializers.CharField(max_length=255)
    tempo = serializers.IntegerField()
    instrument = serializers.CharField(max_length=255)
    rhythm = serializers.CharField(max_length=255)
    sheet_composition = serializers.ListField(default=[])

    def validate(self, attrs):

        return super().validate(attrs)


class CreateSwarVistarSerializer(serializers.Serializer):
    scale = serializers.CharField()
    tempo = serializers.IntegerField()
    instrument = serializers.CharField()
    rhythm = serializers.CharField()

    def validate(self, attrs):
        return super().validate(attrs)


class TaalSerializer(serializers.Serializer):
    taal_name = serializers.CharField()

    def validate(self, attrs):
        return super().validate(attrs)


class GetAudiosSerializer(serializers.Serializer):
    limit = serializers.IntegerField(default=10)
    offset = serializers.IntegerField(default=0)
    search = serializers.CharField(max_length=255, default="")
    sort_col = serializers.CharField(default="id")
    sort_dir = serializers.CharField(default="-")


class AudioScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioScore
        fields = "__all__"
