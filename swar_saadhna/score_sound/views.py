from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils.algo import generate_audios_algo
from .serializers import TaalSerializer, CreateAudiosSerializers

# Create your views here.
from .handlers import AudioHandler


class Audios(APIView):
    def get(self, request):
        return AudioHandler.get_audios(request)

    def post(self, request):
        return AudioHandler.create_audio(request)


class Taal(APIView):
    def get(self, request):
        data = [
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
            "dha",
        ]
        return Response(data)
