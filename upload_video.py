import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
TOKEN_FILE = 'token.json'
SECRETS_FILE = 'client_secrets.json'


def get_credentials():
    creds = None
    # 이전에 로그인한 토큰이 있으면 재사용
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None  # 토큰 만료 시 다시 로그인
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0, open_browser=False)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return creds


def upload_video(file_path, title, description, tags, made_for_kids=True, privacy='private'):
    youtube = build('youtube', 'v3', credentials=get_credentials())

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '1',
        },
        'status': {
            'privacyStatus': privacy,
            # 아동용 콘텐츠면 반드시 True
            'selfDeclaredMadeForKids': made_for_kids,
        },
    }

    media = MediaFileUpload(file_path, chunksize=8 * 1024 * 1024, resumable=True)
    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f'업로드 {int(status.progress() * 100)}%')

    print(f"  업로드 완료! https://youtube.com/shorts/{response['id']}")
    return response['id']


if __name__ == '__main__':
    # 사용법: python3 upload_video.py 영상파일.mp4
    video = sys.argv[1] if len(sys.argv) > 1 else 'my_video.mp4'
    upload_video(
        file_path=video,
        title='Test Upload',
        description='Test upload from Juhee Channel Uploader.',
        tags=['test'],
    )
