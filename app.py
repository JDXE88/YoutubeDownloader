from flask import Flask, request, jsonify, render_template
import yt_dlp as youtube_dl
import os
import subprocess

app = Flask(__name__)

def download_youtube_content(video_url, output_directory, content_type='video', convert_to_mp3=False, audio_format='mp3', audio_quality='0', download_subtitles=False, sub_lang='', download_mp4=False, download_subtitles_only=False):
    """
    Downloads YouTube content in the best quality available and handles optional conversions and subtitles.
    """
    ydl_opts = {
        'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
        'subtitleslangs': [sub_lang] if download_subtitles and sub_lang else None,
        'writesubtitles': download_subtitles and not download_subtitles_only,
        'writeautomaticsub': download_subtitles and not sub_lang and not download_subtitles_only,  # Auto-generated subtitles if no specific language is selected
        'skip_download': content_type == 'subtitles' and not download_subtitles_only,  # Skip download for subtitles-only
    }

    if content_type == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
        if convert_to_mp3:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': audio_quality,
            }]
    elif content_type == 'video':
        if download_mp4:
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'  # Download as MP4 directly
        else:
            ydl_opts['format'] = 'bestvideo+bestaudio/best'  # Download best video and audio
    elif content_type == 'subtitles':
        ydl_opts['writesubtitles'] = True
        ydl_opts['skip_download'] = True

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info_dict)
        
        # Handle subtitle-only download
        if content_type == 'subtitles':
            subtitle_files = [f for f in os.listdir(output_directory) if f.endswith('.vtt')]
            if subtitle_files:
                return os.path.join(output_directory, subtitle_files[0])
            else:
                raise Exception("No subtitles available for this video.")

        # Convert video to MP4 if not downloaded as MP4
        if content_type == 'video' and not download_mp4 and not filename.endswith('.mp4'):
            convert_video(filename, output_directory, 'mp4')

def convert_video(input_file, output_directory, output_format):
    """
    Converts video to specified format using ffmpeg.
    """
    output_file = os.path.join(output_directory, os.path.splitext(os.path.basename(input_file))[0] + f'.{output_format}')
    subprocess.run(['ffmpeg', '-i', input_file, output_file], check=True)
    os.remove(input_file)  # Remove the original file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get('videoUrl')
    output_directory = data.get('outputDirectory')
    content_type = data.get('contentType')
    convert_to_mp3 = data.get('convertToMp3')
    audio_format = data.get('audioFormat')
    audio_quality = data.get('audioQuality')
    download_subtitles = data.get('downloadSubtitles')
    sub_lang = data.get('subLang')
    download_mp4 = data.get('downloadMp4')
    download_subtitles_only = data.get('downloadSubtitlesOnly')

    if not video_url or not output_directory:
        return jsonify({'message': 'Please fill out all fields.'}), 400

    try:
        if content_type == 'subtitles' and not download_subtitles_only:
            # Handle the subtitles-only download
            subtitle_file = download_youtube_content(
                video_url, 
                output_directory, 
                content_type, 
                convert_to_mp3, 
                audio_format, 
                audio_quality, 
                download_subtitles, 
                sub_lang,
                download_mp4,
                download_subtitles_only
            )
            if not os.path.exists(subtitle_file):
                return jsonify({'message': 'No subtitles available for this video.'}), 404
        else:
            download_youtube_content(
                video_url, 
                output_directory, 
                content_type, 
                convert_to_mp3, 
                audio_format, 
                audio_quality, 
                download_subtitles, 
                sub_lang,
                download_mp4,
                download_subtitles_only
            )
        
        return jsonify({'message': f"{content_type.capitalize()} download complete."})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)