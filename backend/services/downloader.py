import yt_dlp
import os

def download_video(url: str, output_dir: str = "temp"):
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        'format': 'worst[ext=mp4]', # Download worst quality to save time/bandwidth
        'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        # Anti-bot measures
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        # Additional options to avoid detection
        'nocheckcertificate': True,
        'no_check_certificate': True,
        'prefer_insecure': False,
        'age_limit': None,
        # Retry options
        'retries': 10,
        'fragment_retries': 10,
        'skip_unavailable_fragments': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return {
                "id": info['id'],
                "title": info['title'],
                "description": info['description'],
                "thumbnail": info['thumbnail'],
                "duration": info['duration'],
                "file_path": f"{output_dir}/{info['id']}.mp4"
            }
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        if "Sign in to confirm" in error_msg or "bot" in error_msg.lower():
            raise Exception(
                "YouTubeからのダウンロードがブロックされました。"
                "この動画は制限がかかっている可能性があります。"
                "別の動画で試すか、しばらく時間をおいてから再度お試しください。"
            )
        else:
            raise Exception(f"動画のダウンロードに失敗しました: {error_msg}")
    except Exception as e:
        raise Exception(f"予期しないエラーが発生しました: {str(e)}")
