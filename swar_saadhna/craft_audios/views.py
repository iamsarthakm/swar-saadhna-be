from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import create_audio_using_notations
class Create(APIView):
    def get(self, request):
        create_audio_using_notations()
        return Response("data", status.HTTP_200_OK)