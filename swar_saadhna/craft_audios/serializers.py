from rest_framework import serializers


class CreateAudiosSerializers(serializers.Serializer):
    scale = serializers.CharField()
    tempo = serializers.IntegerField()
    intrument = serializers.CharField()
    rhythm = serializers.CharField()
    sheet_composition = serializers.ListField(default=[])

    def validate(self, attrs):
        return super().validate(attrs)
