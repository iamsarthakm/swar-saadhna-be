from rest_framework.response import Response
from rest_framework import status
from .utils.algo import generate_audios_algo
from .serializers import (
    CreateAudioSerializers,
    AudioScoreSerializer,
    GetAudioSerializer,
    CreateTaalSerializer,
    GetCompositionSerializer,
    CreateCompositionSerializer,
)
from .utils.utils import (
    get_music_data,
    save_to_s3,
    get_user_id_from_token,
    get_audio_util,
    get_composition_util,
    create_composition_util,
)
from .models import AudioScore, Taal, Composition
import os
import uuid


class AudioHandler:
    def get_audios(request):
        validate_data = GetAudioSerializer(data=request.query_params)
        if not validate_data.is_valid():
            return Response(
                {"message": validate_data.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_id = get_user_id_from_token(request)
        audios_data = get_audio_util(user_id, validate_data.validated_data)
        return Response(audios_data, status=status.HTTP_200_OK)

    def create_audio(request):
        validate_data = CreateAudioSerializers(data=request.data)
        if not validate_data.is_valid():
            return Response(
                {"message": validate_data.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        name, scale, tempo, instrument, composition_id = get_music_data(
            validate_data.validated_data, request
        )
        composition_obj = Composition.objects.filter(id=composition_id).first()
        rhythm = composition_obj.rhythm
        composition = composition_obj.notes_and_beats
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
            composition_id=composition_id,
            user_id=user_id,
            audio_url=audio_url,
        )
        serializer = AudioScoreSerializer(audio_obj_details)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaalHandler:
    def get_taal(request):
        name = request.query_params["name"]
        taal = Taal.objects.filter(name=name).first()
        return Response(taal.beats, status=status.HTTP_200_OK)

    def create_taal(request):
        validate_data = CreateTaalSerializer(data=request.data)
        if not validate_data.is_valid():
            return Response(
                {"message": validate_data.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        name = validate_data.validated_data["name"]
        beats = validate_data.validated_data["beats"]
        taal = Taal.objects.create(name=name, beats=beats)
        return Response(taal.name, status=status.HTTP_200_OK)


class CompositionHandler:
    def get_composition(request):
        validate_data = GetCompositionSerializer(data=request.query_params)
        if not validate_data.is_valid():
            return Response(
                {"message": validate_data.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_id = get_user_id_from_token(request)
        audios_data = get_composition_util(user_id, validate_data.validated_data)
        return Response(audios_data, status=status.HTTP_200_OK)

    def create_composition(request):
        validate_data = CreateCompositionSerializer(data=request.data)
        if not validate_data.is_valid():
            return Response(
                {"message": validate_data.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_id = get_user_id_from_token(request)
        audios_data = create_composition_util(user_id, validate_data.validated_data)
        return Response(audios_data, status=status.HTTP_200_OK)
