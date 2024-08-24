# YoutubeDownloader

A Python application to download YouTube videos or audio in the highest quality.

## Requirements

Before you can use this application, you need to install the following dependencies:

- Flask
- yt-dlp
- ffmpeg

Install Flask and yt-dlp using pip:

```bash
pip install Flask
pip install yt-dlp
```

Install ffmpeg:
- **On Linux**: `sudo apt-get install ffmpeg`
- **On macOS**: `brew install ffmpeg`

## Setup

If you encounter errors related to file permissions or directory access, especially on Linux or Termux, you might need to adjust the permissions of your output directory.

For example, in Termux, you can set the correct permissions using:

```bash
chmod 777 /data/data/com.termux/files/home/storage/shared/Download
```

Make sure to use the absolute path rather than a relative path. To find the absolute path, use the `pwd` command:

```bash
pwd
```

This will print the absolute path of the current directory, which you can then use to specify the output directory in the application.

## Usage

1. **Start the Application**: Run the application by executing the script. Ensure that your server is running and accessible.

2. **Access the Interface**: Open your web browser and navigate to the local server address (usually `http://localhost:5000`).

3. **Enter Details**:
    - **YouTube Video URL**: Provide the full URL of the YouTube video you want to download.
    - **Output Directory**: Specify the directory where the downloaded files will be saved.
    - **Download Type**: Choose between downloading video, audio, or subtitles only.
    - **Audio Options** (if applicable): Configure options for audio downloads, such as conversion to MP3 and format.
    - **Video Options** (if applicable): Select options for video downloads, such as downloading in MP4 format and including subtitles.

4. **Download**: Click the 'Download' button to start the process. The progress of the download will be displayed.

## Troubleshooting

- Ensure you have the correct permissions for the output directory.
- Verify that the YouTube URL and directory path are correctly entered.
- Check the application logs or console output for specific error messages.

For any additional issues, refer to the documentation of the dependencies or seek help from the relevant communities.