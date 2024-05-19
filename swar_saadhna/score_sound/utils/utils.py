import jwt
from django.conf import settings
import boto3
from botocore.exceptions import ClientError
from score_sound.models import AudioScore


def get_music_data(data, request):
    scale = data["scale"]
    name = data["name"]
    tempo = data["tempo"]
    instrument = data["instrument"]
    rhythm = data["rhythm"]
    composition = data["sheet_composition"]
    return name, scale, tempo, instrument, rhythm, composition


def generate_presigned_url(object_key, expiration=3600):
    s3_client = boto3.client(
        "s3",
        region_name=settings.REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.BUCKET_NAME, "Key": object_key},
            ExpiresIn=expiration,
        )
        return presigned_url
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None


def save_to_s3(file_path, key):
    s3_client = boto3.client(
        "s3",
        region_name=settings.REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    try:
        s3_client.upload_file(file_path, Bucket=settings.BUCKET_NAME, Key=key)
        print(f"Data successfully saved to S3://{settings.BUCKET_NAME}/{key}")
        return key
    except Exception as e:
        print(f"Error uploading data to S3: {e}")


def get_user_id_from_token(request):
    token = request.headers.get("Authorization")
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, verify=True, algorithms=["HS256"]
    )
    return payload.get("id", None)


def get_audio_util(user_id, params):
    search = params["search"]
    offset = params["offset"]
    limit = params["limit"]
    order = params["sort_dir"] + params["sort_col"]
    print(user_id)
    audios_list = (
        AudioScore.objects.filter(name__icontains=search, user__id=user_id)
        .order_by(order)
        .values()[offset : limit + offset]
    )

    for audios in audios_list:
        if audios["audio_url"]:
            audios["presigned_url"] = None
        else:
            audios["presigned_url"] = None
    return audios_list



