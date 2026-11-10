"""
'올릴영상' 폴더에 있는 영상을 차례로 유튜브 쇼츠로 올리고,
올린 영상은 '올린영상' 폴더로 옮깁니다.

영상마다 제목/설명을 정하고 싶으면 영상과 같은 이름의 .txt 파일을 옆에 두세요.
  예) puppy_colors.mp4 + puppy_colors.txt
  .txt 첫 줄 = 제목, 나머지 줄 = 설명
  '태그:'로 시작하는 줄이 있으면 쉼표로 나눠 태그로 씁니다.
.txt가 없으면 파일 이름이 제목이 됩니다.
"""
import csv
import datetime
import shutil
import subprocess
from pathlib import Path

from upload_video import upload_video

# ===== 설정 =====
QUEUE_DIR = Path('올릴영상')
DONE_DIR = Path('올린영상')
LOG_FILE = Path('업로드기록.csv')
MAX_PER_RUN = 2          # 한 번 실행에 올릴 최대 개수 (대량 업로드는 수익화 정책에 걸릴 수 있어요)
PRIVACY = 'private'      # 감사 통과 전에는 private만 가능. 통과 후 'public'으로 바꾸세요
DEFAULT_TAGS = ['kids', 'toddler', 'shorts']
VIDEO_EXT = {'.mp4', '.mov', '.m4v'}
# ================


def read_meta(video: Path):
    title = video.stem.replace('_', ' ')
    description = ''
    tags = list(DEFAULT_TAGS)
    txt = video.with_suffix('.txt')
    if txt.exists():
        lines = txt.read_text(encoding='utf-8').splitlines()
        body = []
        for i, line in enumerate(lines):
            if i == 0 and line.strip():
                title = line.strip()
            elif line.strip().startswith('태그:'):
                tags = [t.strip() for t in line.split(':', 1)[1].split(',') if t.strip()]
            else:
                body.append(line)
        description = '\n'.join(body).strip()
    if '#shorts' not in title.lower():
        title = f'{title} #Shorts'
    return title[:100], description[:4900], tags


def is_short(video: Path):
    """세로 영상이고 3분 이하인지 확인 (ffprobe가 없으면 확인 생략)"""
    try:
        out = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
             '-show_entries', 'stream=width,height:format=duration', '-of', 'csv=p=0', str(video)],
            capture_output=True, text=True, timeout=30).stdout.split()
        w, h = map(int, out[0].split(','))
        dur = float(out[1])
        return h >= w and dur <= 180, f'{w}x{h}, {dur:.0f}초'
    except Exception:
        return True, '확인 생략'


def main():
    QUEUE_DIR.mkdir(exist_ok=True)
    DONE_DIR.mkdir(exist_ok=True)
    videos = sorted(p for p in QUEUE_DIR.iterdir() if p.suffix.lower() in VIDEO_EXT)
    if not videos:
        print("'올릴영상' 폴더가 비어 있어요. 영상을 넣고 다시 실행하세요.")
        return

    print(f'대기 중인 영상 {len(videos)}개, 이번에 최대 {MAX_PER_RUN}개 올립니다.\n')
    for video in videos[:MAX_PER_RUN]:
        ok, info = is_short(video)
        if not ok:
            print(f'[건너뜀] {video.name} ({info}) 세로 3분 이하가 아니라 쇼츠가 안 돼요.')
            continue
        title, desc, tags = read_meta(video)
        print(f'[업로드] {video.name} ({info})\n  제목: {title}')
        try:
            vid = upload_video(str(video), title, desc, tags, privacy=PRIVACY)
        except Exception as e:
            print(f'  실패: {e}\n')
            continue
        shutil.move(str(video), DONE_DIR / video.name)
        txt = video.with_suffix('.txt')
        if txt.exists():
            shutil.move(str(txt), DONE_DIR / txt.name)
        new = not LOG_FILE.exists()
        with LOG_FILE.open('a', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f)
            if new:
                w.writerow(['올린시각', '파일', '제목', '링크', '공개상태'])
            w.writerow([datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                        video.name, title, f'https://youtube.com/shorts/{vid}', PRIVACY])
        print()

    left = len([p for p in QUEUE_DIR.iterdir() if p.suffix.lower() in VIDEO_EXT])
    print(f'끝! 남은 영상 {left}개. 기록은 업로드기록.csv에 있어요.')


if __name__ == '__main__':
    main()
