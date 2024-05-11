from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils.algo import generate_audios_algo
from .serializers import (
    CreateAudiosSerializers,
    AudioScoreSerializer,
    GetAudiosSerializer,
)
from .utils.utils import (
    get_music_data,
    save_to_s3,
    get_user_id_from_token,
    get_audio_util,
)
from .models import AudioScore
import os
import uuid


class AudioHandler:
    def get_audios(request):
        validate_data = GetAudiosSerializer(data=request.query_params)
        if not validate_data.is_valid():
            return Response(
                {"message": validate_data.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_id = get_user_id_from_token(request)
        audios_data = get_audio_util(user_id, validate_data.validated_data)
        return Response(audios_data, status=status.HTTP_200_OK)

    def create_audio(request):
        validate_data = CreateAudiosSerializers(data=request.data)
        if not validate_data.is_valid():
            return Response(
                {"message": validate_data.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        name, scale, tempo, instrument, rhythm, composition = get_music_data(
            validate_data.validated_data, request
        )
        user_id = get_user_id_from_token(request)
        temp_audio_path = generate_audios_algo(
            scale, tempo, instrument, rhythm, composition, name
        )

        audio_url = save_to_s3(
            temp_audio_path, f"saved-media/{name}-{uuid.uuid4()}.wav"
        )
        os.remove(temp_audio_path)
        audio_obj_details = AudioScore.objects.create(
            name=name,
            scale=scale,
            tempo=tempo,
            rhythm=rhythm,
            composition=composition,
            user_id=user_id,
            audio_url=audio_url,
        )
        serializer = AudioScoreSerializer(audio_obj_details)
        return Response(serializer.data, status=status.HTTP_200_OK)
