from rest_framework.views import APIView
from .handlers import AudioHandler, TaalHandler


class Audios(APIView):
    def get(self, request):
        return AudioHandler.get_audios(request)

    def post(self, request):
        return AudioHandler.create_audio(request)

    def put(self, request):
        return AudioHandler.edit_audio(request)


class Taal(APIView):
    def get(self, request):
        return TaalHandler.get_taal(request)

    def post(self, request):
        return TaalHandler.create_taal(request)
