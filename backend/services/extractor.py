import ffmpeg
import os

def extract_frame(video_path: str, timestamp: float, output_path: str):
    try:
        (
            ffmpeg
            .input(video_path, ss=timestamp)
            .output(output_path, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return True
    except ffmpeg.Error as e:
        print(f"Error extracting frame: {e.stderr.decode()}")
        return False
