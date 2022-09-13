import boto3
from decouple import config
from smart_open import open as smart_opener
import base64
from chat_app_backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def DefaultAvatarTryExceptBlock(user, profile):
    try:
        with smart_opener(f's3://bucketeer-0f6cb5f5-34a1-49a1-ab57-f884d7245601/bucketeer-0f6cb5f5-34a1-49a1-ab57'
                          f'-f884d7245601/media/public/avatars/{user.username}_default_avatar{profile.extension_default_avatar()}',
                          "rb",
                          transport_params={
                              'client':
                                  session.client(
                                      's3')}) \
                as image_file_2:
            encoded_default_avatar = base64.b64encode(image_file_2.read())
    except:

        with open('avatars/default_avatar.png', "rb") as image_file:
            encoded_default_avatar = base64.b64encode(image_file.read())

    return encoded_default_avatar

def RealAvatarTryExceptBlock(user, profile):
    try:
        with smart_opener(f's3://bucketeer-0f6cb5f5-34a1-49a1-ab57-f884d7245601/bucketeer-0f6cb5f5-34a1-49a1-ab57'
                          f'-f884d7245601/media/public/real_avatars/{user.username}_real_avatar{profile.extension_real_avatar()}',
                          "rb",
                          transport_params={
                              'client':
                                  session.client(
                                      's3')}) \
                as image_file_2:
            encoded_real_avatar = base64.b64encode(image_file_2.read())
    except:
        with open('avatars/default_avatar.png', "rb") as image_file:
            encoded_real_avatar = base64.b64encode(image_file.read())

    return encoded_real_avatar
