import boto3
from decouple import config
from smart_open import open as smart_opener
import base64
AWS_ACCESS_KEY_ID = config('BUCKETEER_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('BUCKETEER_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('BUCKETEER_BUCKET_NAME')
AWS_S3_REGION_NAME = config('BUCKETEER_AWS_REGION')
session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def AvatarsTryExceptBlock(user, profile):
    print('Avatar filename:')
    print(f'{user.username}_default_avatar{profile.extension()}')
    try:
        with smart_opener(f's3://bucketeer-0f6cb5f5-34a1-49a1-ab57-f884d7245601/bucketeer-0f6cb5f5-34a1-49a1-ab57'
                          f'-f884d7245601/media/public/avatars/{user.username}_default_avatar{profile.extension()}',
                          "rb",
                          transport_params={
                              'client':
                                  session.client(
                                      's3')}) \
                as image_file_2:
            encoded_default_avatar = base64.b64encode(image_file_2.read())
    except:
        print('default avatar try failed')
        with open('avatars/default_avatar.png', "rb") as image_file:
            encoded_default_avatar = base64.b64encode(image_file.read())

    try:
        with smart_opener(f's3://bucketeer-0f6cb5f5-34a1-49a1-ab57-f884d7245601/bucketeer-0f6cb5f5-34a1-49a1-ab57'
                          f'-f884d7245601/media/public/real_avatars/{user.username}_real_avatar{profile.extension()}',
                          "rb",
                          transport_params={
                              'client':
                                  session.client(
                                      's3')}) \
                as image_file_2:
            encoded_real_avatar = base64.b64encode(image_file_2.read())
    except:
        print('real avatar try failed')
        with open('avatars/default_avatar.png', "rb") as image_file:
            encoded_real_avatar = base64.b64encode(image_file.read())

    return encoded_default_avatar, encoded_real_avatar