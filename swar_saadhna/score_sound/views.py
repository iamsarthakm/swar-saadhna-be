from rest_framework.views import APIView
from .handlers import AudioHandler, TaalHandler, CompositionHandler


class Composition(APIView):
    def get(self, request):
        return CompositionHandler.get_composition(request)

    def post(self, request):
        return CompositionHandler.create_composition(request)


class Audios(APIView):
    def get(self, request):
        return AudioHandler.get_audios(request)

    def post(self, request):
        return AudioHandler.create_audio(request)


class Taal(APIView):
    def get(self, request):
        return TaalHandler.get_taal(request)

    def post(self, request):
        return TaalHandler.create_taal(request)
