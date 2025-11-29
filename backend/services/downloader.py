import yt_dlp
import os

def download_video(url: str, output_dir: str = "temp"):
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        'format': 'worst[ext=mp4]', # Download worst quality to save time/bandwidth
        'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
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
