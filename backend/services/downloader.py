import yt_dlp
import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def download_video(url: str, output_dir: str = "temp"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. yt-dlp for Metadata Only (Skip Download)
    ydl_opts = {
        'skip_download': True, # Important: Do not download video
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    video_id = None
    metadata = {}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info['id']
            metadata = {
                "id": info['id'],
                "title": info['title'],
                "description": info['description'],
                "thumbnail": info['thumbnail'],
                "duration": info['duration'],
                "file_path": None, # No video file
                "subtitles": ""
            }
    except Exception as e:
        print(f"yt-dlp metadata fetch failed: {e}")
        # Fallback: Try to extract ID from URL manually if yt-dlp fails
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        
        if not video_id:
            raise Exception("動画情報の取得に失敗しました。URLを確認してください。")
        
        # Minimal metadata fallback
        metadata = {
            "id": video_id,
            "title": "YouTube Video", # Placeholder
            "description": "",
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            "duration": 0,
            "file_path": None,
            "subtitles": ""
        }

    # 2. Get Transcripts (Subtitles)
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get Japanese, then English, then auto-generated
        try:
            transcript = transcript_list.find_transcript(['ja', 'en'])
        except NoTranscriptFound:
            # Fallback to auto-generated if available
            transcript = transcript_list.find_generated_transcript(['ja', 'en'])
            
        transcript_data = transcript.fetch()
        
        # Format transcripts into a single string with timestamps
        full_text = ""
        for entry in transcript_data:
            start = int(entry['start'])
            text = entry['text']
            full_text += f"[{start}s] {text}\n"
            
        metadata["subtitles"] = full_text
        print(f"Successfully fetched subtitles for {video_id}")

    except (TranscriptsDisabled, NoTranscriptFound):
        print("No subtitles found. Using description only.")
        metadata["subtitles"] = "(字幕が見つかりませんでした。動画の説明文のみを使用します。)\n" + metadata["description"]
    except Exception as e:
        print(f"Subtitle fetch failed: {e}")
        metadata["subtitles"] = "(字幕取得エラー。動画の説明文のみを使用します。)\n" + metadata["description"]

    return metadata
