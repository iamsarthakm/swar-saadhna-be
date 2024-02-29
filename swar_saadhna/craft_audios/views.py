from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_audios
from .serializers import CreateAudiosSerializers


class Create(APIView):
    def post(self, request):
        validate_data = CreateAudiosSerializers(data=request.data)
        if not validate_data.is_valid():
            return Response(
                {"message": "file_generated_successfully"},
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        generate_audios(validate_data.validated_data)
        return Response("data", status.HTTP_200_OK)
